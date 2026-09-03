#!/usr/bin/env ruby

require "csv"

ROOT = File.expand_path("..", __dir__)
rows = CSV.read(File.join(ROOT, "text/translation-status.csv"), headers: true)

promoted = %w[approved laid-out proofed final]
compact = []

def complete_collation_authority?(root, row)
  source_range = row["source_range"].to_s.match(/^(\d+)\.(\d+)-(\d+)$/)
  return false unless source_range

  first_line = source_range[2].to_i
  expected_end = source_range[3].to_i
  volume_root = File.join(root, "text", row["volume"])
  prefix = "book-#{format('%02d', row['book'].to_i)}-collation-"
  candidates = Dir.glob(File.join(volume_root, "#{prefix}*.md"))
    .each_with_object([]) do |path, matches|
      match = File.basename(path).match(/collation-(\d+)-(\d+)\.md$/)
      next unless match
      matches << [match[1].to_i, match[2].to_i, path]
    end
    .sort_by(&:first)

  cursor = first_line
  return false if candidates.empty? || candidates.first[0] != cursor
  candidates.each do |start_line, end_line, path|
    return false unless start_line == cursor
    return false unless File.read(path).match?(/^## Revised translation pass\s*$/)
    cursor = end_line + 1
  end
  cursor - 1 == expected_end
end

rows.each do |row|
  next if row["status"] == "outline"

  path = File.join(ROOT, row["translation_file"])
  text = File.read(path)
  if text.match?(/compact translation|compact pass|compressed prose/i)
    if complete_collation_authority?(ROOT, row)
      puts "OK #{row['volume']} Book #{row['book']}: full revised collation authority assembled"
    else
      compact << [row["volume"], row["book"], row["status"], row["translation_file"]]
    end
  end
end

compact.each do |volume, book, status, file|
  if promoted.include?(status)
    warn "FAIL: #{volume} Book #{book} (#{file}) is #{status} but still marked as compact or compressed"
    exit 1
  end
  puts "HOLD #{volume} Book #{book}: compact/compressed translation remains editorial material"
end

puts "Translation completeness preflight passed: #{compact.length} compact holds are not promoted."
