# frozen_string_literal:true

require 'csv'
require 'google/apis/civicinfo_v2'
require 'erb'

def clean_zip_code(zip_code)
  zip_code.to_s.rjust(5, '0')[0..4]
end

def fetch_legislators(zip_code)
  civic_info = Google::Apis::CivicinfoV2::CivicInfoService.new
  civic_info.key = 'AIzaSyClRzDqDh5MsXwnCWi0kOiiBivP6JsSyBw'
  begin
    civic_info.representative_info_by_address(
      address: zip_code,
      levels: 'country',
      roles: ['legislatorUpperBody', 'legislatorLowerBody']
    ).officials
  rescue
    'You can find your representatives by visiting www.commoncause.org/take-action/find-elected-officials'
  end
end

def save_thank_you_letter(id,form_letter)
  Dir.mkdir('output') unless Dir.exist?('output')

  filename = "output/thanks_#{id}.html"

  File.open(filename, 'w') do |file|
    file.puts form_letter
  end
end

puts 'event manager initialized'
filename = 'event_attendees.csv'

content = CSV.open(
  filename,
  headers: true,
  header_converters: :symbol
)

template_letter = File.read('form_letter.erb')
erb_template = ERB.new template_letter

content.each do |row|
  id = row[0]
  name = row[:first_name]

  zip_code = clean_zip_code(row[:zipcode])

  legislators = fetch_legislators(zip_code)

  form_letter = erb_template.result(binding)

  save_thank_you_letter(id, form_letter)
end
