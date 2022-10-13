import pytest
import recommender
import pandas as pd
from pandas import Index
import numpy as np

data = {
    "title": {
        0: "The Hunger Games",
        1: "Harry Potter and the Order of the Phoenix",
        2: "To Kill a Mockingbird",
        3: "Pride and Prejudice",
        4: "Twilight",
    },
    "author": {
        0: "Suzanne Collins",
        1: "J.K. Rowling",
        2: "Harper Lee",
        3: "Jane Austen",
        4: "Stephenie Meyer",
    },
    "rating": {0: 4.33, 1: 4.5, 2: 4.28, 3: 4.26, 4: 3.6},
    "description": {
        0: "WINNING MEANS FAME AND FORTUNE.LOSING MEANS CERTAIN DEATH.THE HUNGER GAMES HAVE BEGUN. . . .In the ruins of a place once known as North America lies the nation of Panem, a shining Capitol surrounded by twelve outlying districts. The Capitol is harsh and cruel and keeps the districts in line by forcing them all to send one boy and once girl between the ages of twelve and eighteen to participate in the annual Hunger Games, a fight to the death on live TV.Sixteen-year-old Katniss Everdeen regards it as a death sentence when she steps forward to take her sister's place in the Games. But Katniss has been close to dead before—and survival, for her, is second nature. Without really meaning to, she becomes a contender. But if she is to win, she will have to start making choices that weight survival against humanity and life against love.",
        1: "There is a door at the end of a silent corridor. And it’s haunting Harry Pottter’s dreams. Why else would he be waking in the middle of the night, screaming in terror?Harry has a lot on his mind for this, his fifth year at Hogwarts: a Defense Against the Dark Arts teacher with a personality like poisoned honey; a big surprise on the Gryffindor Quidditch team; and the looming terror of the Ordinary Wizarding Level exams. But all these things pale next to the growing threat of He-Who-Must-Not-Be-Named - a threat that neither the magical government nor the authorities at Hogwarts can stop.As the grasp of darkness tightens, Harry must discover the true depth and strength of his friends, the importance of boundless loyalty, and the shocking price of unbearable sacrifice.His fate depends on them all.",
        2: "The unforgettable novel of a childhood in a sleepy Southern town and the crisis of conscience that rocked it, To Kill A Mockingbird became both an instant bestseller and a critical success when it was first published in 1960. It went on to win the Pulitzer Prize in 1961 and was later made into an Academy Award-winning film, also a classic.Compassionate, dramatic, and deeply moving, To Kill A Mockingbird takes readers to the roots of human behavior - to innocence and experience, kindness and cruelty, love and hatred, humor and pathos. Now with over 18 million copies in print and translated into forty languages, this regional story by a young Alabama woman claims universal appeal. Harper Lee always considered her book to be a simple love story. Today it is regarded as a masterpiece of American literature.",
        3: 'Alternate cover edition of ISBN 9780679783268Since its immediate success in 1813, Pride and Prejudice has remained one of the most popular novels in the English language. Jane Austen called this brilliant work "her own darling child" and its vivacious heroine, Elizabeth Bennet, "as delightful a creature as ever appeared in print." The romantic clash between the opinionated Elizabeth and her proud beau, Mr. Darcy, is a splendid performance of civilized sparring. And Jane Austen\'s radiant wit sparkles as her characters dance a delicate quadrille of flirtation and intrigue, making this book the most superb comedy of manners of Regency England.',
        4: "About three things I was absolutely positive.\n\nFirst, Edward was a vampire.\n\nSecond, there was a part of him—and I didn't know how dominant that part might be—that thirsted for my blood.\n\nAnd third, I was unconditionally and irrevocably in love with him.\n\nDeeply seductive and extraordinarily suspenseful, Twilight is a love story with bite.",
    },
    "language": {0: "English", 1: "English", 2: "English", 3: "English", 4: "English"},
    "isbn": {
        0: "9780439023481",
        1: "9780439358071",
        2: "9999999999999",
        3: "9999999999999",
        4: "9780316015844",
    },
    "genres": {0: "fiction", 1: "fantasy", 2: "thriller", 3: "fiction", 4: "fantasy"},
    "numRatings": {0: 6376780, 1: 2507623, 2: 4501075, 3: 2998241, 4: 4964519},
    "likedPercent": {0: 96.0, 1: 98.0, 2: 95.0, 3: 94.0, 4: 78.0},
    "coverImg": {
        0: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1586722975l/2767052.jpg",
        1: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1546910265l/2.jpg",
        2: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1553383690l/2657.jpg",
        3: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1320399351l/1885.jpg",
        4: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1361039443l/41865.jpg",
    },
}


@pytest.fixture
def dataframe():
    return pd.DataFrame(data)


def test_preprocess_data(dataframe):
    df = recommender.preprocess_data(dataframe)
    assert type(df) == pd.DataFrame
    assert (
        df.columns.all()
        == Index(
            ["fantasy", "fiction", "thriller", "rating", "numRatings"], dtype="object"
        ).all()
    )


df_1 = pd.DataFrame(
    {
        "fantasy": {0: 0, 1: 1, 2: 0, 3: 0, 4: 1},
        "fiction": {0: 1, 1: 0, 2: 0, 3: 1, 4: 0},
        "thriller": {0: 0, 1: 0, 2: 1, 3: 0, 4: 0},
        "rating": {0: 4.33, 1: 4.5, 2: 4.28, 3: 4.26, 4: 3.6},
        "numRatings": {0: 6376780, 1: 2507623, 2: 4501075, 3: 2998241, 4: 4964519},
    }
)


@pytest.mark.parametrize(
    "raw,normalized",
    [
        (
            df_1,
            np.array(
                [
                    [0.0, 1.0, 0.0, 0.81111111, 1.0],
                    [1.0, 0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 1.0, 0.75555556, 0.51521611],
                    [0.0, 1.0, 0.0, 0.73333333, 0.1268023],
                    [1.0, 0.0, 0.0, 0.0, 0.63499517],
                ],
            ),
        )
    ],
)
def test_normalize_data(raw, normalized):
    assert type(recommender.normalize_data(raw)) == np.ndarray
    assert recommender.normalize_data(raw).all() == normalized.all()
