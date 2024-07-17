from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

from flask_app.models.commet import Comment

class Manga:
    def __init__(self, data):
        self.id = data["id"]
        self.subject = data["subject"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

        self.user_name = data["user_name"]
        self.comments = []

    @classmethod
    def save_manga(cls, form):
        query = "insert into posts (content, subject, user_id) values (%(content)s, 'manga', %(user_id)s)"
        return connectToMySQL("foro_publicaciones").query_db(query, form)
    
    @staticmethod
    def validate_post_manga(form):
        is_valid = True

        if len(form["content"]) < 1:
            flash("Post content is required", "post")
            is_valid = False

        return is_valid
    
    @classmethod
    def get_manga(cls):
        query = "SELECT posts.*, users.first_name as user_name FROM posts JOIN users ON posts.user_id = users.id WHERE subject = 'manga' ORDER BY created_at DESC ;"
        results = connectToMySQL("foro_publicaciones").query_db(query) 
        posts = []
        for p in results: 
            post = cls(p)
            query_comments = "SELECT comments.*, users.first_name as user_name FROM comments JOIN users ON comments.user_id = users.id WHERE post_id = %(post_id)s"
            data_comment = {"post_id": p["id"]} 
            results_comments = connectToMySQL("foro_publicaciones").query_db(query_comments, data_comment)
            comments = []
            for c in results_comments:
                comments.append(Comment(c)) 
            post.comments = comments 
            posts.append(post)
        return posts
       
    @classmethod
    def delete_manga(cls, data):
        query = "delete from posts where id = %(id)s"
        connectToMySQL("foro_publicaciones").query_db(query, data)