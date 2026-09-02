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

generated_manifest = path_from_root("assets/generated/manifest.csv")
rows = CSV.read(generated_manifest, headers: true)

rows.each_with_index do |row, index|
  row_number = index + 2
  file = row["final_file"]
  fail!("generated manifest row #{row_number} has no final_file") if file.nil? || file.empty?

  image_path = path_from_root(file)
  fail!("missing generated asset #{file} (row #{row_number})") unless File.file?(image_path)

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
