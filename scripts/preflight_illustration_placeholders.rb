#!/usr/bin/env ruby

ROOT = File.expand_path("..", __dir__)
PATH = File.join(ROOT, "design", "illustration-placeholders.md")

def fail!(message)
  warn "FAIL illustration placeholders: #{message}"
  exit 1
end

fail!("missing #{PATH}") unless File.file?(PATH)

records = File.read(PATH).each_line.each_with_object([]) do |line, found|
  match = line.match(/^\|\s*(ILI|ODY)-(\d{2})\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$/)
  next unless match
  found << { slot: "#{match[1]}-#{match[2]}", volume: match[1], book: match[3].to_i,
             anchor: match[4], prompt: match[5] }
end

fail!("expected 48 placeholder rows, found #{records.length}") unless records.length == 48
fail!("duplicate slot IDs") unless records.map { |record| record[:slot] }.uniq.length == 48

%w[ILI ODY].each do |volume|
  books = records.select { |record| record[:volume] == volume }.map { |record| record[:book] }.sort
  fail!("#{volume} placeholders do not cover Books 1–24") unless books == (1..24).to_a
end

records.each do |record|
  fail!("#{record[:slot]} has no source anchor") if record[:anchor].empty?
  fail!("#{record[:slot]} has no prompt text") if record[:prompt].empty?
  fail!("#{record[:slot]} lacks exact-range caution") unless record[:anchor].match?(/canonical source range:/i)
  fail!("#{record[:slot]} prompt lacks original-work/provenance direction") unless
    record[:prompt].match?(/original|historical|Blake-informed/i)
end

puts "Illustration placeholder preflight passed: 48 unique book prompts with source-range and provenance direction."
