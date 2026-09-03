#!/usr/bin/env ruby

require "csv"

ROOT = File.expand_path("..", __dir__)

def fail!(message)
  warn "FAIL read-aloud coverage: #{message}"
  exit 1
end

ledger = CSV.read(File.join(ROOT, "text", "translation-status.csv"), headers: true)
fail!("translation ledger must contain 48 books") unless ledger.length == 48

checked = 0
ledger.each do |row|
  volume = row["volume"]
  book = row["book"].to_i
  stem = "#{volume}-book-#{format('%02d', book)}"
  packet_path = File.join(ROOT, "text", "reviews", "#{stem}.md")
  log_path = File.join(ROOT, "text", "reviews", "#{stem}-read-aloud.md")
  fail!("missing packet #{packet_path}") unless File.file?(packet_path)
  fail!("missing read-aloud log #{log_path}") unless File.file?(log_path)

  packet = File.read(packet_path)
  log = File.read(log_path)
  fail!("#{packet_path} does not identify read-aloud evidence") unless packet.match?(/read[- ]aloud/i)
  fail!("#{log_path} has no scope declaration") unless log.match?(/\*\*Scope:\*\*|Review status:/i)
  fail!("#{log_path} has no critical findings") unless log.match?(/Findings|Changes made|Read-aloud observations|Observations?|Action/i)
  fail!("#{log_path} does not preserve human review as pending") unless log.match?(/human (?:sign[- ]?off|reader)|independent (?:reader|.*human)/i)

  checked += 1
  puts "OK #{volume} Book #{book}: read-aloud log and human-review hold present"
end

puts "Read-aloud preflight passed: #{checked} book-level logs are present and explicitly non-final."
