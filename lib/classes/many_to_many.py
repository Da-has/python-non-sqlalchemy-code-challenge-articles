class Article:
    """Represents an Article written by an Author for a Magazine."""
    all = []

    def __init__(self, author, magazine, title):
        if not isinstance(author, Author):
            raise TypeError("author must be an Author instance")
        if not isinstance(magazine, Magazine):
            raise TypeError("magazine must be a Magazine instance")
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("title must be a string between 5 and 50 characters")

        self._title = title
        self.author = author
        self.magazine = magazine

        Article.all.append(self)

    @property
    def title(self):
        """Title is immutable after initialization."""
        return self._title

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise TypeError("author must be an Author instance")
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise TypeError("magazine must be a Magazine instance")
        self._magazine = value


class Author:
    """Represents an Author who can write multiple articles for multiple magazines."""

    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("name must be a non-empty string")
        self._name = name

    @property
    def name(self):
        """Author name is immutable."""
        return self._name

    def articles(self):
        """Return all articles written by this author."""
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        """Return unique magazines the author has contributed to."""
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
        """Create and associate a new Article with this author and given magazine."""
        if not isinstance(magazine, Magazine):
            raise TypeError("magazine must be a Magazine instance")
        return Article(self, magazine, title)

    def topic_areas(self):
        """Return unique categories of magazines the author has contributed to or None."""
        arts = self.articles()
        if not arts:
            return None
        return list({article.magazine.category for article in arts})


class Magazine:
    """Represents a Magazine which can publish multiple articles by multiple authors."""
    all = []

    def __init__(self, name, category):
        self.name = name
        self.category = category
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("name must be a string between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("category must be a non-empty string")
        self._category = value

    def articles(self):
        """Return all articles published in this magazine."""
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        """Return unique authors who have written for this magazine."""
        return list({article.author for article in self.articles()})

    def article_titles(self):
        """Return a list of titles for all articles, or None if none."""
        arts = self.articles()
        return [article.title for article in arts] if arts else None

    def contributing_authors(self):
        """Return authors with more than 2 articles in this magazine, or None."""
        arts = self.articles()
        if not arts:
            return None
        counts = {}
        for article in arts:
            counts[article.author] = counts.get(article.author, 0) + 1
        result = [author for author, count in counts.items() if count > 2]
        return result if result else None

    @classmethod
    def top_publisher(cls):
        """Return the magazine with the most articles, or None if no articles exist."""
        if not Article.all:
            return None
        return max(cls.all, key=lambda mag: len(mag.articles()))
