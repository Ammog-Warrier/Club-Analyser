class Club:
    def __init__(self, name, group, whatsapp_msgs, whatsapp_members,
                 insta_posts, insta_likes, insta_comments, insta_followers,
                 events, votes, collaborations):
        self.name = name
        self.group = group
        self.whatsapp_msgs = whatsapp_msgs
        self.whatsapp_members = whatsapp_members
        self.insta_posts = insta_posts
        self.insta_likes = insta_likes
        self.insta_comments = insta_comments
        self.insta_followers = insta_followers
        self.events = events
        self.votes = votes
        self.collaborations = collaborations
        self.composite_score = 0