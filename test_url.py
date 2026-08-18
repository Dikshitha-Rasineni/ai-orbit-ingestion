from src.normalization.url import normalize_url


test_url = "[https://github.com/AMAI-GmbH/AI-Expert-Roadmap](https://github.com/AMAI-GmbH/AI-Expert-Roadmap)"

result = normalize_url(test_url)

print("Input:")
print(test_url)

print("\nOutput:")
print(result)

print("\nExpected:")
print("https://github.com/AMAI-GmbH/AI-Expert-Roadmap")

print("\nCorrect:", result == "https://github.com/AMAI-GmbH/AI-Expert-Roadmap")