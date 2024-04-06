import os
from docx import Document
from chatwoot import Chatwoot


def read_docx(file_path):
    """
    Read a .docx file and return its text content.
    """
    try:
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading .docx file: {e}")
        return None


def create_article_file(article_content, file_path):
    # Function to create an article file
    with open(file_path, 'w', encoding='utf-8') as article_file:
        article_file.write(article_content.strip())

def create_path(directory):
    # Function to create a directory path
    if not os.path.exists(directory):
        os.makedirs(directory)
    
def split_and_save_articles_to_disk(file_path):
    content = read_docx(file_path)
    if content is None:
        return

    # Splitting the document into articles
    articles = content.split("Chat Path:")

    # Checking and creating a directory for saved articles
    if not os.path.exists('articles'):
        os.makedirs('articles')

    # Saving each article in a separate file
    for i, article in enumerate(articles[2:]):
        rows =  article.split('\n')

        path = rows[0]
        path = path.split(" / ")

        title = path[-1]
        title = title.replace('/', '\\')


        path = path[:-1]
        # Create subdirectories based on the path
        subdirectory = os.path.join('articles', *path)
        if not os.path.exists(subdirectory):
            os.makedirs(subdirectory)


        article = '\n'.join(rows[1:])

        # remove the "Assistant: "word
        article = article.replace("Assistant: ", '', 1)

        article_file_name = os.path.join(subdirectory, f'{title}.md')
        with open(article_file_name, 'w', encoding='utf-8') as article_file:
            article_file.write(article.strip())

def create_categorie_tree(category_tree):
    chatwoot = Chatwoot()
    parent_category = None
    for category in category_tree:
        slug = Chatwoot.sluggify(category)
        chatwoot.add_category(
            description = category,
            name = category,
            slug= slug,
            parent_category_id=parent_category
        )
        parent_category = slug
    return parent_category

def split_and_save_articles(file_path):
    content = read_docx(file_path)
    if content is None:
        return

    # Splitting the document into articles
    articles = content.split("Chat Path:")

    chatwoot = Chatwoot()
    # Saving each article in a separate file
    for _, article in enumerate(articles[2:]):
        rows =  article.split('\n')

        category_tree = rows[0]
        category_tree = category_tree.split(" / ")

        title = category_tree[-1]
        title = title.replace('/', '\\')

        category_tree = category_tree[:-1]
        print(category_tree)

        categorie = create_categorie_tree(category_tree)

        # get id from categorie slug
        categorie_ids = chatwoot.get_categories()
        categorie_id = categorie_ids[categorie]

        article = '\n'.join(rows[1:])

        # # remove the "Assistant: "word
        article = article.replace("Assistant: ", '', 1)

        # create article usingarticle title categorie
        chatwoot.add_article(title, article, categorie_id)

def publish_all():
    chatwoot = Chatwoot()
    article_ids = chatwoot.list_articles()
    for article_id in article_ids:
        chatwoot.publish_article(article_id)



# Replace './docs/mydoc.docx' with the path to your document
split_and_save_articles('./docs/33b14984-52a7-4f9a-9a39-6a1831006acd.docx')
publish_all()