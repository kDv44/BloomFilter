import unittest
import random
import string

from main import BloomFilter


email_domains = [
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "aol.com",
    "outlook.com",
    "icloud.com",
    "mail.com",
    "zoho.com",
]


def generate_random_emails(num_names):
    emails = set()

    while len(emails) < num_names:
        name = "".join(random.choices(string.ascii_lowercase, k=8))
        domain = random.choice(email_domains)
        email = f"{name}@{domain}"
        emails.add(email)

    return list(emails)


class TestBloomFilter(unittest.TestCase):
    def setUp(self):
        self.size = 1000000
        self.number_expected_elements = 100000
        self.bloom_filter = BloomFilter(
            size=self.size, number_expected_elements=self.number_expected_elements
        )


    def test_add_and_check_elements(self):
        emails = generate_random_emails(1000)
        for email in emails:
            self.bloom_filter.add_to_filter(email)

        for email in emails:
            self.assertTrue(
                self.bloom_filter.check(email), f"Expected {email} to be in the filter"
            )


    def test_check_non_existent_elements(self):
        emails = generate_random_emails(100000)
        for email in emails:
            self.bloom_filter.add_to_filter(email)

        non_existent_numbers = [
            str(random.randint(-(10**6), 10**6)) for _ in range(1000)
        ]

        for num in non_existent_numbers:
            self.assertTrue(
                self.bloom_filter.check_is_not_in_filter(num),
                f"Expected {num} to be definitely not in the filter",
            )


if __name__ == "__main__":
    unittest.main()
