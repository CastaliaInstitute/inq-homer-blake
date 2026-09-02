#!/usr/bin/env ruby

require "csv"
require "open3"

ROOT = File.expand_path("..", __dir__)
MIN_DPI = 300.0

def fail!(message)
  warn "FAIL: #{message}"
  exit 1
end

def path_from_root(path)
  File.expand_path(path, ROOT)
end

status_manifest = path_from_root("text/translation-status.csv")
status_rows = CSV.read(status_manifest, headers: true)
fail!("translation status ledger must contain 48 books") unless status_rows.length == 48
valid_statuses = %w[outline draft review approved laid-out proofed final]
valid_reviews = %w[pending pass revise]
status_rows.each_with_index do |row, index|
  row_number = index + 2
  fail!("status ledger row #{row_number} has invalid status") unless valid_statuses.include?(row["status"])
  %w[greek_review narrative_review verse_review diction_review notes_review production_review].each do |field|
    fail!("status ledger row #{row_number} has invalid #{field}") unless valid_reviews.include?(row[field])
  end
end
puts "OK translation status ledger: #{status_rows.length} books"

generated_manifest = path_from_root("assets/generated/manifest.csv")
rows = CSV.read(generated_manifest, headers: true)

source_manifest = path_from_root("assets/source/manifest.csv")
CSV.read(source_manifest, headers: true).each_with_index do |row, index|
  row_number = index + 2
  %w[creator creator_role work_title collection_or_source_url rights_status credit_line].each do |field|
    fail!("source manifest row #{row_number} is missing #{field}") if row[field].nil? || row[field].empty?
  end
  if row["local_file"] && !row["local_file"].empty?
    fail!("missing source asset #{row['local_file']} (row #{row_number})") unless File.file?(path_from_root(row["local_file"]))
  end
end
puts "OK source manifest and acquired files"

rows.each_with_index do |row, index|
  row_number = index + 2
  file = row["final_file"]
  fail!("generated manifest row #{row_number} has no final_file") if file.nil? || file.empty?

  image_path = path_from_root(file)
  fail!("missing generated asset #{file} (row #{row_number})") unless File.file?(image_path)

  prompt_file = row["prompt_file"]
  fail!("generated manifest row #{row_number} has no prompt_file") if prompt_file.nil? || prompt_file.empty?
  fail!("missing prompt record #{prompt_file} (row #{row_number})") unless File.file?(path_from_root(prompt_file))

  width_output, status = Open3.capture2("sips", "-g", "pixelWidth", "-g", "pixelHeight", image_path)
  fail!("cannot inspect #{file} with sips") unless status.success?
  width = width_output[/pixelWidth:\s*(\d+)/, 1].to_i
  height = width_output[/pixelHeight:\s*(\d+)/, 1].to_i
  fail!("no dimensions found for #{file}") if width.zero? || height.zero?

  # The project trim is 7 × 10 inches. A concept may be below print resolution,
  # but a record marked final may not pass this gate.
  dpi = [width / 7.0, height / 10.0].min
  if row["curation_status"] == "final" && dpi < MIN_DPI
    fail!("final asset #{file} is #{dpi.round(1)} dpi; minimum is #{MIN_DPI.to_i} dpi")
  end
  puts "OK #{file}: #{width}x#{height}, #{dpi.round(1)} dpi, status=#{row['curation_status']}"
end

puts "Asset preflight passed."
