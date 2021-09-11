from user_location import UserLocation

def main():
    user_location = "    53453+  "
    ul = UserLocation()
    country = ul.locator(user_location)
    print(f"The country for {user_location} is {country}")

if __name__ == "__main__":
    main()