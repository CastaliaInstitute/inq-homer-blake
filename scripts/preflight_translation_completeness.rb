#!/usr/bin/env ruby

require "csv"

ROOT = File.expand_path("..", __dir__)
rows = CSV.read(File.join(ROOT, "text/translation-status.csv"), headers: true)

promoted = %w[approved laid-out proofed final]
compact = []

rows.each do |row|
  next if row["status"] == "outline"

  path = File.join(ROOT, row["translation_file"])
  text = File.read(path)
  if text.match?(/compact translation|compact pass|compressed prose/i)
    compact << [row["volume"], row["book"], row["status"], row["translation_file"]]
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
