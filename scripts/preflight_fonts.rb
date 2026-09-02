#!/usr/bin/env ruby

require "digest"

ROOT = File.expand_path("..", __dir__)

LOCKED = {
  "assets/fonts/CormorantGaramond-Regular.ttf" => "7c1aace7373d5603eb520713a8d69e71e7ed75ca95965cb3872f6a74c399eff9",
  "assets/fonts/CormorantGaramond-SemiBold.ttf" => "4fcd2d97820dac2be5f9c24d7fbd264a08f89b16a0d12fcc80541b3fbd44ee92",
  "assets/fonts/CormorantGaramond-Italic.ttf" => "6458bdd71b7ffaa7e2bf44a3ff66d2bb49de4841958d853cfcb779c7b1ddc890",
  "assets/fonts/OFL.txt" => "60700d351cac4650c51f3f9db318d2a420f8b45052dba2715eb5fec41f0f6956"
}

LOCKED.each do |relative, expected|
  path = File.join(ROOT, relative)
  abort("FAIL font lock: missing #{relative}") unless File.file?(path)
  actual = Digest::SHA256.file(path).hexdigest
  abort("FAIL font lock: #{relative} has #{actual}, expected #{expected}") unless actual == expected
end

license = File.read(File.join(ROOT, "assets/fonts/OFL.txt"))
abort("FAIL font lock: OFL 1.1 text missing") unless license.include?("SIL OPEN FONT LICENSE Version 1.1")
abort("FAIL font lock: font lock documentation missing") unless File.file?(File.join(ROOT, "design/font-lock.md"))

puts "OK fonts: Cormorant Garamond files and OFL 1.1 checksum lock verified"
