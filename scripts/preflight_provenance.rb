#!/usr/bin/env ruby

require "csv"
require "digest"

ROOT = File.expand_path("..", __dir__)

def fail!(message)
  warn "FAIL: #{message}"
  exit 1
end

plate_file = File.join(ROOT, "design", "plate-manifest.csv")
source_file = File.join(ROOT, "assets", "source", "manifest.csv")
generated_file = File.join(ROOT, "assets", "generated", "manifest.csv")

plates = CSV.read(plate_file, headers: true)
sources = CSV.read(source_file, headers: true)
generated = CSV.read(generated_file, headers: true)

plate_ids = {}
plate_files = {}

plates.each do |row|
  id = row["plate_id"]
  fail!("duplicate plate_id #{id}") if plate_ids[id]
  plate_ids[id] = true
  fail!("#{id}: missing provenance URL") if row["provenance_url"].to_s !~ %r{\Ahttps://}
  fail!("#{id}: missing rights status") if row["rights_status"].to_s.strip.empty?
  fail!("#{id}: missing caption") if row["caption"].to_s.strip.empty?
  fail!("#{id}: missing credit line") if row["credit_line"].to_s.strip.empty?
  path = row["final_file"].to_s
  fail!("#{id}: missing local file #{path}") unless File.file?(File.join(ROOT, path))
  fail!("#{id}: local file is already assigned to #{plate_files[path]}") if plate_files[path]
  plate_files[path] = id
  if row["source_type"] == "historical-reference"
    fail!("#{id}: historical plate must say it is not a Blake composition") unless row["credit_line"].include?("not a Blake composition") || row["credit_line"].include?("Blake is not credited")
    fail!("#{id}: historical credit must identify Flaxman as designer") unless row["credit_line"].include?("John Flaxman") && row["credit_line"].include?("designer")
    fail!("#{id}: Blake must be identified only as engraver when named") if row["creator"].include?("William Blake") && !row["creator_role"].include?("engraver")
  elsif row["source_type"] == "generated"
    fail!("#{id}: generated plate must identify original work") unless row["credit_line"].include?("Original") && row["credit_line"].include?("not by William Blake")
    fail!("#{id}: generated plate must be credited to CastaliaInstitute") unless row["creator"] == "CastaliaInstitute"
    fail!("#{id}: generated plate must point to a prompt record") unless row["prompt_or_source_record"].start_with?("assets/generated/prompts/")
  else
    fail!("#{id}: unknown source type #{row['source_type']}")
  end
end

sources.each do |row|
  fail!("source #{row['local_file']}: blank creator") if row["creator"].to_s.strip.empty?
  fail!("source #{row['local_file']}: missing object number") if row["object_number"].to_s.strip.empty?
end

generated.each do |row|
  fail!("generated #{row['final_file']}: missing prompt record") unless File.file?(File.join(ROOT, row["prompt_file"].to_s))
  fail!("generated #{row['final_file']}: missing original-work credit") unless row["credit_line"].to_s.include?("Original") && row["credit_line"].to_s.include?("not by William Blake")
end

prompt_files = Dir[File.join(ROOT, "assets", "generated", "prompts", "*.md")]
prompt_files.each do |path|
  fail!("#{path}: ambiguous a.Blake shorthand; use Blake-informed or a named creator role") if File.read(path).include?("a.Blake")
end

puts "OK provenance: #{plates.length} plates have sources, rights, captions, credits, and local files"
