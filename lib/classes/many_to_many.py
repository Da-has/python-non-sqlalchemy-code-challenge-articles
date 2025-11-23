class Article:
    all = []
    def __init__(self, author, magazine, title):
        # Validating our inputs to ensure no invalid objects or strings
        if not isinstance(author, Author):
            raise TypeError("author must be an Author instance")
        if not isinstance(magazine, Magazine):
            raise TypeError("magazine must be a Magazine instance")
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("title must be a string between 5 and 50 characters")

        # Instance variables
        self._author = author
        self._magazine = magazine
        self._title = title

        # Registering the article with author and the magazine
        author._articles.append(self)
        magazine._articles.append(self)

        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_author):
        if not isinstance(new_author, Author):
            raise TypeError("author must be an Author instance")
        # Remove from old author's articles list
        if self in self._author._articles:
            self._author._articles.remove(self)
        # Assign new author and add to their articles list
        self._author = new_author
        new_author._articles.append(self)

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, new_magazine):
        if not isinstance(new_magazine, Magazine):
            raise TypeError("magazine must be a Magazine instance")
        # Remove from old magazine's articles list
        if self in self._magazine._articles:
            self._magazine._articles.remove(self)
        # Assign new magazine and add to its articles list
        self._magazine = new_magazine
        new_magazine._articles.append(self)

class Author:
    def __init__(self, name):
        # Validating the name
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("name must be a non-empty string")
        
        self._name = name
        self._articles = []  # List of Article instances

    @property
    def name(self):
        return self._name

    # Return all articles by an author
    def articles(self):
        return self._articles

    # Return unique magazines the author has contributed to.
    def magazines(self):
        # Avoiding any form of duplicates (using list comprehension)
        return list({article.magazine for article in self._articles})

    # Add new article
    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    # Return any unique categories of magazines that an author contributed to
    def topic_areas(self):
        if not self._articles:
            return None
        return list({article.magazine.category for article in self._articles})
    
class Magazine:
    all_magazines = [] #list of magazines

    def __init__(self, name, category):
        # Validation of inputes
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("name must be a string between 2 and 16 characters")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("category must be a non-empty string")

        self._name = name
        self._category = category
        self._articles = []  # List of Article instances published in this magazine

        # Register this magazine in the global scope
        Magazine.all_magazines.append(self)

    # A name property that's mutable
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str) or not (2 <= len(new_name) <= 16):
            raise ValueError("name must be a string between 2 and 16 characters")
        self._name = new_name

    # A category property that's mutable
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if not isinstance(new_category, str) or len(new_category) == 0:
            raise ValueError("category must be a non-empty string")
        self._category = new_category

    def articles(self):
        return self._articles

    def contributors(self):
        return list({article.author for article in self._articles})

    def article_titles(self):
        if not self._articles:
            return None
        return [article.title for article in self._articles]

    # Return authors with more than 2 articles in this magazine.
    def contributing_authors(self):
        if not self._articles:
            return None
        from collections import Counter
        author_counts = Counter(article.author for article in self._articles)
        authors = [author for author, count in author_counts.items() if count > 2]
        return authors if authors else None

    #  A class method that will return the magazine with the most articles.
    @classmethod
    def top_publisher(cls):
        if not cls.all_magazines:
            return None
        return max(cls.all_magazines, key=lambda mag: len(mag._articles))
