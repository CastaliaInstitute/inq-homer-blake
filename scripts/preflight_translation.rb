#!/usr/bin/env ruby

require "csv"

ROOT = File.expand_path("..", __dir__)
ledger = File.join(ROOT, "text/translation-status.csv")
rows = CSV.read(ledger, headers: true)

def fail!(message)
  warn "FAIL: #{message}"
  exit 1
end

rows.each_with_index do |row, index|
  row_number = index + 2
  status = row["status"]
  file = row["translation_file"]
  if status == "outline"
    fail!("outline row #{row_number} must not point to a translation file") unless file.nil? || file.empty?
    next
  end

  fail!("#{status} row #{row_number} has no translation_file") if file.nil? || file.empty?
  path = File.join(ROOT, file)
  fail!("missing translation file #{file} (row #{row_number})") unless File.file?(path)
  content = File.read(path)
  %w[# **Source passage:** ## Translation ## Decision log].each do |marker|
    fail!("#{file} (row #{row_number}) is missing #{marker}") unless content.include?(marker)
  end
  if %w[draft review].include?(status)
    unless content.match?(/Greek-fidelity review|Greek-fidelity gate|review task|Draft warning/i)
      fail!("#{file} (row #{row_number}) has no explicit unresolved review warning")
    end
  end
  puts "OK #{file}: #{status}"
end

puts "Translation structure preflight passed: #{rows.length} books."
