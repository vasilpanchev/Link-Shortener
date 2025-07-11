from link_shortener import LinkShortener


print("Enter a URL to shorten (e.g., 'https://example.com'):")
link = input().strip().rstrip('/')
link_shortener = LinkShortener(link)
success, message = link_shortener.generate_shortened_link()
print("✅" if success else "❌", message)