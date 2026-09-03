#!/usr/bin/env ruby

# Heuristic guard against promoting a short synopsis as a complete translation.
# Density is triage evidence only: a human editor may waive an outlier with a
# documented reason, but the ledger must not promote it silently.

require "csv"

ROOT = File.expand_path("..", __dir__)
MIN_WORDS_PER_SOURCE_LINE = 5.0
PROMOTED = %w[approved laid-out proofed final]

def effective_translation(path, text)
  return text unless text.match?(/compact translation/i)
  authorities = Dir.glob(File.join(File.dirname(path), "#{File.basename(path).sub('-opening.md', '')}-collation-*.md")).sort
  bodies = authorities.each_with_object([]) do |candidate, collected|
    candidate_text = File.read(candidate)
    match = candidate_text.match(/^## Revised translation pass\s*\n(.*?)(?=^## Decision|\z)/m)
    collected << match[1] if match
  end
  bodies.empty? ? text : "## Translation\n#{bodies.join("\n\n")}"
end

ledger = CSV.read(File.join(ROOT, "text/translation-status.csv"), headers: true)
rows = []
holds = []

ledger.each do |record|
  next if record["status"] == "outline"

  path = File.join(ROOT, record["translation_file"])
  text = File.read(path)
  ranges = text.scan(/\*\*Source passage:\*\* Book \d+, lines (\d+)[–-](\d+)/)
  abort("#{record['translation_file']} has no parseable source passage") if ranges.empty?

  translation = effective_translation(path, text)[/^## Translation\s*(.*?)(?=^## Decision log\b|\z)/m, 1].to_s
  # Match translation_extract.book_translation: section labels are structural
  # metadata, not reader-facing verse, and Python's \w includes the same
  # Unicode letters/digits we accept here.
  reader_text = translation.lines.reject { |line| line.start_with?("#") }.join
  words = reader_text.scan(/\b[\p{L}\p{N}_’'-]+\b/u).length
  source_start = ranges.map { |start_line, _| start_line.to_i }.min
  source_end = ranges.map { |_, end_line| end_line.to_i }.max
  source_lines = source_end - source_start + 1
  density = words.to_f / source_lines
  row = [record["volume"], record["book"], record["status"], record["translation_file"],
         source_lines, words, format("%.2f", density), density < MIN_WORDS_PER_SOURCE_LINE ? "hold" : "screen-pass"]
  rows << row
  holds << row if density < MIN_WORDS_PER_SOURCE_LINE
end

if rows.length != 48
  abort("expected 48 translation rows, found #{rows.length}")
end

holds.each do |volume, book, status, file, *_|
  if PROMOTED.include?(status)
    abort("#{file} is #{status} but falls below the #{MIN_WORDS_PER_SOURCE_LINE} words/source-line completeness screen")
  end
end

out = File.join(ROOT, "design", "translation-density-report.md")
File.open(out, "w") do |handle|
  handle.puts "# Translation density screen"
  handle.puts
  handle.puts "This is a conservative triage screen, not a literary or Greek-fidelity judgment. It compares the reader-facing Translation sections against their declared source ranges. A hold flags material compression for expansion or a documented editorial waiver before promotion. Threshold: **#{MIN_WORDS_PER_SOURCE_LINE} English words per source line**."
  handle.puts
  handle.puts "| Volume | Book | Status | Source lines | English words | Words/source line | Result |"
  handle.puts "|---|---:|---|---:|---:|---:|---|"
  rows.each do |volume, book, status, file, source_lines, words, density, result|
    handle.puts "| #{volume} | #{book} | #{status} | #{source_lines} | #{words} | #{density} | #{result} |"
  end
  handle.puts
  handle.puts "**Current holds:** #{holds.length} of 48 books. These books remain provisional and must not be represented as complete final translations solely because their collation files cover the source endpoint."
end

puts "Translation density screen passed: #{holds.length} provisional holds; no promoted book falls below threshold."
