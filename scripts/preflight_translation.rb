#!/usr/bin/env ruby

require "csv"

ROOT = File.expand_path("..", __dir__)
ledger = File.join(ROOT, "text/translation-status.csv")
rows = CSV.read(ledger, headers: true)
coverage = CSV.read(File.join(ROOT, "text/source-coverage.csv"), headers: true)

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

  if %w[review approved laid-out proofed final].include?(status)
    coverage_row = coverage.find do |candidate|
      candidate["volume"] == row["volume"] && candidate["book"].to_i == row["book"].to_i
    end
    fail!("#{file} has no source-coverage row") unless coverage_row
    expected_end = coverage_row["canonical_greek_last_line"].to_i
    intervals = []
    Dir[File.join(ROOT, "text", row["volume"], "book-#{row['book'].to_i.to_s.rjust(2, '0')}-collation-*.md")].each do |collation|
      match = File.basename(collation).match(/collation-(\d+)-(\d+)\.md\z/)
      intervals << [match[1].to_i, match[2].to_i] if match
    end
    cursor = 1
    intervals.sort.each do |start_line, end_line|
      fail!("#{file} has a source-collation gap before line #{start_line}") if start_line > cursor
      cursor = [cursor, end_line + 1].max
    end
    fail!("#{file} source collation ends at #{cursor - 1}, expected #{expected_end}") unless cursor == expected_end + 1
  end

  if %w[approved laid-out proofed final].include?(status)
    gates = %w[greek_review narrative_review verse_review diction_review notes_review production_review]
    fail!("#{file} cannot be #{status} until all six review gates pass") unless gates.all? { |gate| row[gate] == "pass" }
    packet = File.join(ROOT, "text", "reviews", "#{row['volume']}-book-#{row['book'].to_i.to_s.rjust(2, '0')}.md")
    fail!("#{file} is missing signed review packet #{packet}") unless File.file?(packet)
    packet_text = File.read(packet)
    fail!("#{packet} is not marked approved") unless packet_text.match?(/^\*\*Decision:\*\* approved\s*$/)
    fail!("#{packet} has no named reviewer") if packet_text.match?(/^\*\*Reviewer:\*\* unassigned\s*$/)
    fail!("#{packet} has no review date") if packet_text.match?(/^\*\*Review date:\*\* unassigned\s*$/)
  end
  puts "OK #{file}: #{status}"
end

puts "Translation structure preflight passed: #{rows.length} books."
