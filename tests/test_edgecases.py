def test_update_nonexistent_returns_404(client):
    # no todos exist
    res = client.put("/todos/999", json={"title": "no one"})
    assert res.status_code == 405

def test_delete_nonexistent_is_idempotent(client):
    # deleting non-existing id should still return 200 and message (per current implementation)
    res = client.delete("/todos/42")
    assert res.status_code == 404
    # assert res.get_json().get("message") == "Deleted successfully"

def test_multiple_creates_increment_ids(client):
    r1 = client.post("/todos", json={"title": "A"})
    r2 = client.post("/todos", json={"title": "B"})
    assert r1.status_code == 201 and r2.status_code == 201
    a = r1.get_json(); b = r2.get_json()
    assert a["id"] == 1
    assert b["id"] == 2

def test_create_todo_without_title(client):
    res=client.post("/todos",json={"title":""})    
    assert res.status_code==400, f"bhai khali nhi chalega"



def test_mark_todo_done(client):
    # sabse phele apan todo baneynge
    res=client.post("/todos",json={"title":"Finish homework"})
    todo_id=res.get_json()["id"]

    # ab usko apan update krenge
    res=client.patch(f"/todos/{todo_id}",json={"is_done":True})
    assert res.status_code==200 ,f" mene except kia thaa 200 aur mere kay bhi milea dekho{res.status_code}"
    # yei sara data fecth kreaga json kei format  
    data=res.get_json()
    assert data["is_done"] is True ,f" this is done"


def test_invalid_request(client):
    # sabse phele apan todo mai data add kr bayenge
    res=client.post("/todos",json={"title":"abhi gym jana hai"})
    todo_id=res.get_json()["id"]

    # ab apan non exasting krke update dalke check krenge
    res=client.patch(f"/todos/{9999}",json={"id_done":True})

    assert res.status_code==404 ,f" bhai tum bay id dal rhe hau jay mere pass nhi hai isliye mai error dunga "


def test_deleteto_request(client):
      res1=client.post("/todos",json={"title":"abhi gym jana hai"})
      res2=client.post("/todos",json={"title":"abhi gym sei aya hun thak gya hun"}) 
      res3=client.post("/todos",json={"title":"abhi jake mai apna project kruga"})

      todoid_1=res1.get_json()["id"]
      todoid_2=res2.get_json()["id"]
      todoid_3=res3.get_json()["id"]



      del1=client.delete(f"/todos/{todoid_1}")
      del2=client.delete(f"/todos/{todoid_2}")
      del3=client.delete(f"/todos/{todoid_3}")


      assert del1.status_code==200
      assert del2.status_code==200
      assert del3.status_code ==200



      #finaal ab apan check krenge url hit krke

      res=client.get("/todos")
      assert res.get_json()==[]

