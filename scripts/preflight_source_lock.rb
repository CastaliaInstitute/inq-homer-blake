#!/usr/bin/env ruby

ROOT = File.expand_path("..", __dir__)
lock = File.read(File.join(ROOT, "text/source-lock.md"))
sources = File.read(File.join(ROOT, "text/sources.md"))

def fail!(message)
  warn "FAIL: #{message}"
  exit 1
end

required_lock = [
  "urn:cts:greekLit:tlg0012.tlg001.perseus-grc2",
  "urn:cts:greekLit:tlg0012.tlg002.perseus-grc2",
  "ac0bc60033f1f83990a5cf7f1e7fc2e0423e381a",
  "15ab2da1201d6160db741e7806f12667f692d47e5884e216c3bd12b08efa4ce8",
  "246f17cc2e9c3f4e8b97fe7d6fcf56dbc4f34f215d9b1447b2878a6152e0656a",
  "Active drafts: Iliad Books 1–24",
  "Active drafts: Odyssey Books 1–24"
]
required_lock.each do |value|
  fail!("source-lock.md is missing #{value}") unless lock.include?(value)
end

fail!("source-lock.md must use HTTPS retrieval URLs") unless lock.match?(%r{https://raw\.githubusercontent\.com/PerseusDL/canonical-greekLit/})
fail!("source-lock.md must record verification command") unless lock.include?("shasum -a 256")
fail!("sources.md is not aligned to Odyssey grc2") unless sources.include?("tlg0012.tlg002.perseus-grc2")
fail!("sources.md must link the Scaife Odyssey record") unless sources.include?("atlas.perseus.tufts.edu")

puts "OK source lock: Iliad and Odyssey pinned, hashed, and aligned"
