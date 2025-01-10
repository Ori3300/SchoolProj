import DButilities
db = DButilities.DButilities()
import User
import Business
import Comment


if __name__ == "__main__":
    user1 = User.User("ori", "123", None)
    user2 = User.User("shalev", "111", None)
    
    business1 = Business.Business(
        name="Pizzaria",
        category="food",
        description="the best pizza in the world!",
        owner_name= user1.get_username(),
        owner_id= user1.get_id(),
        comments= None
    )
    comment1 = Comment.Comment(user2.get_username(), "So delicius")
    comment2 = Comment.Comment(user2.get_username(), "W")
    
    business2 = Business.Business(
        name="Tech Solutions",
        category="Technology",
        description="A company specializing in software development.",
        owner_name= user1.get_username(),
        owner_id= user1.get_id(),
        comments= None
    )

    comment3 = Comment.Comment(user2.get_username(), "wowwww")
    comment4 = Comment.Comment(user2.get_username(), "You are the king")

    business1.add_comment(comment1)
    business2.add_comment(comment3)
    business1.add_comment(comment2)
    business2.add_comment(comment4)
    user1.add_business(business1)
    user1.add_business(business2)
    user1.add_user_to_DB()

