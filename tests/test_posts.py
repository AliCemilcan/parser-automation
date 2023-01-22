from typing import List

import pytest

from app import schemas


def test_get_all_posts(authorize_client, create_posts):
    res = authorize_client.get("/post")

    def validate(post):
        return schemas.PostOut(**post)

    post_map = map(validate, res.json())
    # print(list(post_map))
    post_list = list(post_map)
    assert post_list[0].Post.id == res.json()[0].get("Post").get("id")
    assert len(res.json()) == len(create_posts)
    assert res.status_code == 200


def test_unauthorized_client_get_401(client):
    res = client.get("/post/12312321")
    assert res.status_code == 404


def test_get_one_post_with_id(authorize_client, create_posts):
    res = authorize_client.get(f"post/{create_posts[0].id}")
    print(":*******", list(create_posts))
    post = schemas.PostOut(**res.json())
    assert post.Post.id == create_posts[0].id


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("awesome", "awesome content", True),
        ("MADO", "I love baklava", True),
        ("HACIBABA", "Iskender", False),
    ],
)
def test_create_post(
    authorize_client,
    test_user,
    create_posts,
    title,
    content,
    published,
):
    res = authorize_client.post(
        "/post",
        json={
            "title": title,
            "content": content,
            "published": published,
            "owner_id": test_user["id"],
        },
    )
    create_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert create_post.title == title
    assert create_post.content == content
    assert create_post.published == published


def test_unauthorized_delete_post(client, test_user, create_posts):
    res = client.delete(f"/post/{create_posts[0].id}")
    assert res.status_code == 401


def test_authorized_delete_post(authorize_client, test_user, create_posts):
    res = authorize_client.delete(f"/post/{create_posts[0].id}")
    assert res.status_code == 204


def test_delete_other_user_post(authorize_client, test_user, test_user2, create_posts):
    res = authorize_client.delete(f"/post/{create_posts[4].id}")
    assert res.status_code == 403
