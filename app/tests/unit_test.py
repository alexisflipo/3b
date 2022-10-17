import pytest
import sklearn
import recommender
import pandas as pd
from pandas import Index
import numpy as np
from sklearn.cluster import KMeans
data = pd.DataFrame(
    {
        "title": {
            0: "The Hunger Games",
            1: "Harry Potter and the Order of the Phoenix",
            5: "The Book Thief",
            14: "The Da Vinci Code",
            16: "The Picture of Dorian Gray",
            41: "The Princess Bride",
            70: "The Bell Jar",
            74: "Outlander",
            86: "Angela's Ashes",
            121: "The Very Hungry Caterpillar",
            163: "The Lorax",
            362: "The Tell-Tale Heart and Other Writings",
            1365: "Steve Jobs",
        },
        "author": {
            0: "Suzanne Collins",
            1: "J.K. Rowling",
            5: "Markus Zusak (Goodreads Author)",
            14: "Dan Brown (Goodreads Author)",
            16: "Oscar Wilde",
            41: "William Goldman",
            70: "Sylvia Plath",
            74: "Diana Gabaldon (Goodreads Author)",
            86: "Frank McCourt",
            121: "Eric Carle",
            163: "Dr. Seuss",
            362: "Edgar Allan Poe",
            1365: "Walter Isaacson (Goodreads Author)",
        },
        "rating": {
            0: 4.33,
            1: 4.5,
            5: 4.37,
            14: 3.86,
            16: 4.08,
            41: 4.26,
            70: 4.01,
            74: 4.23,
            86: 4.11,
            121: 4.3,
            163: 4.34,
            362: 4.17,
            1365: 4.14,
        },
        "description": {
            0: "WINNING MEANS FAME AND FORTUNE.LOSING MEANS CERTAIN DEATH.THE HUNGER GAMES HAVE BEGUN. . . .In the ruins of a place once known as North America lies the nation of Panem, a shining Capitol surrounded by twelve outlying districts. The Capitol is harsh and cruel and keeps the districts in line by forcing them all to send one boy and once girl between the ages of twelve and eighteen to participate in the annual Hunger Games, a fight to the death on live TV.Sixteen-year-old Katniss Everdeen regards it as a death sentence when she steps forward to take her sister's place in the Games. But Katniss has been close to dead before—and survival, for her, is second nature. Without really meaning to, she becomes a contender. But if she is to win, she will have to start making choices that weight survival against humanity and life against love.",
            1: "There is a door at the end of a silent corridor. And it’s haunting Harry Pottter’s dreams. Why else would he be waking in the middle of the night, screaming in terror?Harry has a lot on his mind for this, his fifth year at Hogwarts: a Defense Against the Dark Arts teacher with a personality like poisoned honey; a big surprise on the Gryffindor Quidditch team; and the looming terror of the Ordinary Wizarding Level exams. But all these things pale next to the growing threat of He-Who-Must-Not-Be-Named - a threat that neither the magical government nor the authorities at Hogwarts can stop.As the grasp of darkness tightens, Harry must discover the true depth and strength of his friends, the importance of boundless loyalty, and the shocking price of unbearable sacrifice.His fate depends on them all.",
            5: "Librarian's note: An alternate cover edition can be found hereIt is 1939. Nazi Germany. The country is holding its breath. Death has never been busier, and will be busier still.By her brother's graveside, Liesel's life is changed when she picks up a single object, partially hidden in the snow. It is The Gravedigger's Handbook, left behind there by accident, and it is her first act of book thievery. So begins a love affair with books and words, as Liesel, with the help of her accordian-playing foster father, learns to read. Soon she is stealing books from Nazi book-burnings, the mayor's wife's library, wherever there are books to be found.But these are dangerous times. When Liesel's foster family hides a Jew in their basement, Liesel's world is both opened up, and closed down.In superbly crafted writing that burns with intensity, award-winning author Markus Zusak has given us one of the most enduring stories of our time.(Note: this title was not published as YA fiction)",
            14: "ISBN 9780307277671 moved to this edition.While in Paris, Harvard symbologist Robert Langdon is awakened by a phone call in the dead of the night. The elderly curator of the Louvre has been murdered inside the museum, his body covered in baffling symbols. As Langdon and gifted French cryptologist Sophie Neveu sort through the bizarre riddles, they are stunned to discover a trail of clues hidden in the works of Leonardo da Vinci—clues visible for all to see and yet ingeniously disguised by the painter.Even more startling, the late curator was involved in the Priory of Sion—a secret society whose members included Sir Isaac Newton, Victor Hugo, and Da Vinci—and he guarded a breathtaking historical secret. Unless Langdon and Neveu can decipher the labyrinthine puzzle—while avoiding the faceless adversary who shadows their every move—the explosive, ancient truth will be lost forever.",
            16: "Written in his distinctively dazzling manner, Oscar Wilde’s story of a fashionable young man who sells his soul for eternal youth and beauty is the author’s most popular work. The tale of Dorian Gray’s moral disintegration caused a scandal when it ﬁrst appeared in 1890, but though Wilde was attacked for the novel’s corrupting inﬂuence, he responded that there is, in fact, “a terrible moral in Dorian Gray.” Just a few years later, the book and the aesthetic/moral dilemma it presented became issues in the trials occasioned by Wilde’s homosexual liaisons, which resulted in his imprisonment. Of Dorian Gray’s relationship to autobiography, Wilde noted in a letter, “Basil Hallward is what I think I am: Lord Henry what the world thinks me: Dorian what I would like to be—in other ages, perhaps.",
            41: "What happens when the most beautiful girl in the world marries the handsomest prince of all time and he turns out to be...well...a lot less than the man of her dreams?As a boy, William Goldman claims, he loved to hear his father read the S. Morgenstern classic, The Princess Bride. But as a grown-up he discovered that the boring parts were left out of good old Dad's recitation, and only the \"good parts\" reached his ears.Now Goldman does Dad one better. He's reconstructed the \"Good Parts Version\" to delight wise kids and wide-eyed grownups everywhere.What's it about? Fencing. Fighting. True Love. Strong Hate. Harsh Revenge. A Few Giants. Lots of Bad Men. Lots of Good Men. Five or Six Beautiful Women. Beasties Monstrous and Gentle. Some Swell Escapes and Captures. Death, Lies, Truth, Miracles, and a Little Sex.In short, it's about everything.",
            70: "The Bell Jar chronicles the crack-up of Esther Greenwood: brilliant, beautiful, enormously talented, and successful, but slowly going under—maybe for the last time. Sylvia Plath masterfully draws the reader into Esther's breakdown with such intensity that Esther's insanity becomes completely real and even rational, as probable and accessible an experience as going to the movies. Such deep penetration into the dark and harrowing corners of the psyche is an extraordinary accomplishment and has made The Bell Jar a haunting American classic.",
            74: "The year is 1945. Claire Randall, a former combat nurse, is just back from the war and reunited with her husband on a second honeymoon when she walks through a standing stone in one of the ancient circles that dot the British Isles. Suddenly she is a Sassenach—an “outlander”—in a Scotland torn by war and raiding border clans in the year of Our Lord...1743. Hurled back in time by forces she cannot understand, Claire is catapulted into the intrigues of lairds and spies that may threaten her life, and shatter her heart. For here James Fraser, a gallant young Scots warrior, shows her a love so absolute that Claire becomes a woman torn between fidelity and desire—and between two vastly different men in two irreconcilable lives.",
            86: "Imbued on every page with Frank McCourt's astounding humor and compassion. This is a glorious book that bears all the marks of a classic.\"When I look back on my childhood I wonder how I managed to survive at all. It was, of course, a miserable childhood: the happy childhood is hardly worth your while. Worse than the ordinary miserable childhood is the miserable Irish childhood, and worse yet is the miserable Irish Catholic childhood.\" So begins the Pulitzer Prize winning memoir of Frank McCourt, born in Depression-era Brooklyn to recent Irish immigrants and raised in the slums of Limerick, Ireland. Frank's mother, Angela, has no money to feed the children since Frank's father, Malachy, rarely works, and when he does he drinks his wages. Yet Malachy-- exasperating, irresponsible and beguiling-- does nurture in Frank an appetite for the one thing he can provide: a story. Frank lives for his father's tales of Cuchulain, who saved Ireland, and of the Angel on the Seventh Step, who brings his mother babies. Perhaps it is story that accounts for Frank's survival. Wearing rags for diapers, begging a pig's head for Christmas dinner and gathering coal from the roadside to light a fire, Frank endures poverty, near-starvation and the casual cruelty of relatives and neighbors--yet lives to tell his tale with eloquence, exuberance and remarkable forgiveness. Angela's Ashes, imbued on every page with Frank McCourt's astounding humor and compassion, is a glorious book that bears all the marks of a classic.",
            121: "THE all-time classic story, from generation to generation, sold somewhere in the world every 30 seconds! Have you shared it with a child or grandchild in your life? One sunny Sunday, the caterpillar was hatched out of a tiny egg. He was very hungry. On Monday, he ate through one apple; on Tuesday, he ate through three plums--and still he was hungry. When full at last, he made a cocoon around himself and went to sleep, to wake up a few weeks later wonderfully transformed into a butterfly!The brilliantly innovative Eric Carle has dramatized the story of one of Nature's commonest yet loveliest marvels, the metamorphosis of the butterfly. This audiobook will delight as well as instruct the very youngest listener.",
            163: "\"UNLESS someone like you...cares a whole awful lot...nothing is going to get better...It's not.\" Long before saving the earth became a global concern, Dr. Seuss, speaking through his character the Lorax, warned against mindless progress and the danger it posed to the earth's natural beauty. His classic cautionary tale is now available in an irresistible mini-edition, perfect for backpack or briefcase, for Arbor Day, Earth Day, and every day.",
            362: 'Edgar Allan Poe remains the unsurpassed master of works of mystery and madness in this outstanding collection of Poe\'s prose and poetry are sixteen of his finest tales, including "The Tell-Tale Heart", "The Murders in the Rue Morgue", "The Fall of the House of Usher," "The Pit and the Pendulum," "William Wilson," "The Black Cat," "The Cask of Amontillado," and "Eleonora". Here too is a major selection of what Poe characterized as the passion of his life, his poems - "The Raven," "Annabel Lee," Ulalume," "Lenore," "The Bells," and more, plus his glorious prose poem "Silence - A Fable" and only full-length novel, The Narrative of Arthur Gordon Pym.',
            1365: "Walter Isaacson's \"enthralling\" (The New Yorker) worldwide bestselling biography of Apple cofounder Steve Jobs. Based on more than forty interviews with Steve Jobs conducted over two years--as well as interviews with more than 100 family members, friends, adversaries, competitors, and colleagues--Walter Isaacson has written a riveting story of the roller-coaster life and searingly intense personality of a creative entrepreneur whose passion for perfection and ferocious drive revolutionized six industries: personal computers, animated movies, music, phones, tablet computing, and digital publishing. Isaacson's portrait touched millions of readers. At a time when America is seeking ways to sustain its innovative edge, Jobs stands as the ultimate icon of inventiveness and applied imagination. He knew that the best way to create value in the twenty-first century was to connect creativity with technology. He built a company where leaps of the imagination were combined with remarkable feats of engineering. Although Jobs cooperated with the author, he asked for no control over what was written. He put nothing off-limits. He encouraged the people he knew to speak honestly. He himself spoke candidly about the people he worked with and competed against. His friends, foes, and colleagues offer an unvarnished view of the passions, perfectionism, obsessions, artistry, devilry, and compulsion for control that shaped his approach to business and the innovative products that resulted. His tale is instructive and cautionary, filled with lessons about innovation, character, leadership, and values. Steve Jobs is the inspiration for the movie of the same name starring Michael Fassbender, Kate Winslet, Seth Rogen, and Jeff Daniels, directed by Danny Boyle with a screenplay by Aaron Sorkin.",
        },
        "language": {
            0: "English",
            1: "English",
            5: "English",
            14: "English",
            16: "English",
            41: "English",
            70: "English",
            74: "English",
            86: "English",
            121: "English",
            163: "English",
            362: "English",
            1365: "English",
        },
        "isbn": {
            0: "9780439023481",
            1: "9780439358071",
            5: "9780375831003",
            14: "9999999999999",
            16: "9999999999999",
            41: "9780345418265",
            70: "9999999999999",
            74: "9780440242949",
            86: "9780007205233",
            121: "9780241003008",
            163: "9780679889106",
            362: "9780553212280",
            1365: "9781451648539",
        },
        "genres": {
            0: "fiction",
            1: "fantasy",
            5: "war",
            14: "thriller",
            16: "literature",
            41: "comedy",
            70: "health",
            74: "romance",
            86: "nonfiction",
            121: "food",
            163: "environment",
            362: "horror",
            1365: "tech",
        },
        "numRatings": {
            0: 6376780,
            1: 2507623,
            5: 1834276,
            14: 1933446,
            16: 966196,
            41: 779597,
            70: 591175,
            74: 824014,
            86: 539576,
            121: 396110,
            163: 283383,
            362: 221639,
            1365: 956505,
        },
        "likedPercent": {
            0: 96.0,
            1: 98.0,
            5: 96.0,
            14: 89.0,
            16: 94.0,
            41: 95.0,
            70: 93.0,
            74: 92.0,
            86: 94.0,
            121: 94.0,
            163: 95.0,
            362: 96.0,
            1365: 93.0,
        },
        "coverImg": {
            0: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1586722975l/2767052.jpg",
            1: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1546910265l/2.jpg",
            5: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1522157426l/19063._SY475_.jpg",
            14: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1579621267l/968.jpg",
            16: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1546103428l/5297.jpg",
            41: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1327903636l/21787.jpg",
            70: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1554582218l/6514._SY475_.jpg",
            74: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1529065012l/10964._SY475_.jpg",
            86: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1348317139l/252577.jpg",
            121: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1603739265l/4948._SX318_.jpg",
            163: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1327879938l/7784.jpg",
            362: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1327936583l/391729.jpg",
            1365: "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1511288482l/11084145._SY475_.jpg",
        },
        "bookFormat_encoded": {
            0: "paper_book",
            1: "paper_book",
            5: "paper_book",
            14: "paper_book",
            16: "paper_book",
            41: "paper_book",
            70: "paper_book",
            74: "paper_book",
            86: "paper_book",
            121: "paper_book",
            163: "paper_book",
            362: "paper_book",
            1365: "paper_book",
        },
    }
)

def test_preprocess_data():
    df = recommender.preprocess_data(data)
    assert type(df) == pd.DataFrame
    assert (
        df.columns.all()
        == Index(
            ['comedy', 'environment', 'fantasy', 'fiction', 'food', 'health',
       'horror', 'literature', 'nonfiction', 'romance', 'tech', 'thriller',
       'war', 'rating','numRatings'], dtype="object"
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

def test_generate_df_for_training():
    df = recommender.preprocess_data(data)
    encoded_data = recommender.normalize_data(df)
    df_kmeans = recommender.generate_df_for_training(encoded_data)
    assert type(df_kmeans) == pd.DataFrame
    assert (
        df_kmeans.columns.all()
        == Index(
            ["comedy",
            "environment",
            "fantasy",
            "fiction",
            "health",
            "horror",
            "literature",
            "nonfiction",
            "romance",
            "tech",
            "food",
            "thriller",
            "war",
            "rating",
            "numRatings"], dtype="object"
        ).all()
    )

def test_kmeans_model_elaboration():
    df = recommender.preprocess_data(data)
    encoded_data = recommender.normalize_data(df)
    df_kmeans = recommender.generate_df_for_training(encoded_data)
    kmeans = recommender.kmeans_model_elaboration(encoded_data)
    
    assert type(kmeans) == KMeans