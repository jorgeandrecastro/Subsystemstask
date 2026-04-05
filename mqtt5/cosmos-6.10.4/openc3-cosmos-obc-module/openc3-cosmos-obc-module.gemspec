# encoding: ascii-8bit

Gem::Specification.new do |s|
  s.name = 'openc3-cosmos-obc-module'
  s.summary = 'OpenC3 openc3-cosmos-obc-module plugin'
  s.description = <<-EOF
    openc3-cosmos-obc-module plugin for deployment to OpenC3
  EOF
  s.license = 'MIT'
  s.authors = ['Anonymous']
  s.email = ['name@domain.com']
  s.homepage = 'https://github.com/OpenC3/cosmos'
  s.platform = Gem::Platform::RUBY
  s.required_ruby_version = '>= 3.0'

  if ENV['VERSION']
    s.version = ENV['VERSION'].dup
  else
    time = Time.now.strftime("%Y%m%d%H%M%S")
    s.version = '0.0.0' + ".#{time}"
  end
  
  python_dep_file = File.exist?('pyproject.toml') ? 'pyproject.toml' : 'requirements.txt'
  
  # Utiliser Dir.glob pour trouver tous les fichiers
  all_files = Dir.glob("**/*", File::FNM_DOTMATCH).reject { |f| 
    f.match(%r{^bin/|\.gem$|^(test|spec|features)/}) || File.directory?(f) 
  }
  
  s.files = all_files
end