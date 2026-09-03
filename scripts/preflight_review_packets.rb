#!/usr/bin/env ruby

require "csv"

ROOT = File.expand_path("..", __dir__)

def fail!(message)
  warn "FAIL: #{message}"
  exit 1
end

ledger = CSV.read(File.join(ROOT, "text", "translation-status.csv"), headers: true)
coverage = CSV.read(File.join(ROOT, "text", "source-coverage.csv"), headers: true)
fail!("translation ledger must contain 48 books") unless ledger.length == 48

required_gates = %w[Greek\ fidelity Narrative Verse Diction Notes Production]
packet_count = 0

ledger.each_with_index do |row, index|
  row_number = index + 2
  volume = row["volume"]
  book = row["book"].to_i
  packet_path = File.join(ROOT, "text", "reviews", "#{volume}-book-#{format('%02d', book)}.md")
  fail!("missing review packet #{packet_path} (ledger row #{row_number})") unless File.file?(packet_path)

  packet = File.read(packet_path)
  fail!("#{packet_path} missing source-map register") unless packet.include?("## Source-map register")
  fail!("#{packet_path} missing gate evidence register") unless packet.include?("## Gate evidence register")
  required_gates.each do |gate|
    fail!("#{packet_path} missing #{gate} gate row") unless packet.match?(/^\| #{Regexp.escape(gate)} \|/)
  end

  ledger_gate_fields = {
    "Greek fidelity" => "greek_review",
    "Narrative" => "narrative_review",
    "Verse" => "verse_review",
    "Diction" => "diction_review",
    "Notes" => "notes_review",
    "Production" => "production_review",
  }
  passed_gates = ledger_gate_fields.select { |_, field| row[field] == "pass" }
  unless passed_gates.empty?
    fail!("#{packet_path} records a passed gate without a named reviewer") if packet.match?(/^\*\*Reviewer:\*\*\s*(?:unassigned|)$/i)
    fail!("#{packet_path} records a passed gate without a review date") if packet.match?(/^\*\*Review date:\*\*\s*(?:unassigned|)$/i)
  end

  coverage_row = coverage.find { |candidate| candidate["volume"] == volume && candidate["book"].to_i == book }
  fail!("#{packet_path} has no canonical source-coverage row") unless coverage_row
  expected_end = coverage_row["canonical_greek_last_line"].to_i

  intervals = packet.each_line.each_with_object([]) do |line, found|
    match = line.match(/^\|\s*(\d+)\s*[–-]\s*(\d+)\s*\|\s*\[[^\]]+\]\(([^)]+)\)\s*\|/)
    found << [match[1].to_i, match[2].to_i, match[3]] if match
  end
  fail!("#{packet_path} has no source-map intervals") if intervals.empty?

  cursor = 1
  intervals.sort_by(&:first).each do |start_line, end_line, link|
    fail!("#{packet_path} has an invalid interval #{start_line}-#{end_line}") if end_line < start_line
    fail!("#{packet_path} source-map gap before line #{start_line}") if start_line > cursor
    target = File.expand_path(link, File.dirname(packet_path))
    fail!("#{packet_path} links to missing authority #{link}") unless File.file?(target)
    authority = File.read(target)
    has_translation_authority = authority.include?("## Revised translation pass") ||
      authority.match?(/English location|Revised translation/i) ||
      authority.match?(/## (?:Editorial )?decisions\b/i)
    fail!("#{target} has no translation/collation authority section") unless has_translation_authority
    fail!("#{target} has no pinned Greek source") unless authority.match?(/Perseus(?:DL)?|canonical Greek|source-lock\.md|Greek copy text/i)
    has_checksum = authority.match?(/SHA-256\s*:\s*`[^`]+`|SHA-256\s*\n\s*`[^`]+`/)
    has_source_revision = authority.match?(/(?:Source|Perseus) revision:|\*\*Source lock:\*\*|source-lock\.md/i)
    fail!("#{target} has no source revision or checksum") unless has_checksum || has_source_revision
    cursor = [cursor, end_line + 1].max
  end
  fail!("#{packet_path} source map ends at #{cursor - 1}, expected #{expected_end}") unless cursor == expected_end + 1

  packet_count += 1
  puts "OK #{volume} Book #{book}: #{intervals.length} contiguous source-map interval(s)"
end

puts "Review-packet preflight passed: #{packet_count} packets cover their canonical source spans."
