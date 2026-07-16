from ssl_checker import check_ssl

print("Google:")
print(check_ssl("https://google.com"))

print("\nDVWA:")
print(check_ssl("http://localhost/dvwa"))