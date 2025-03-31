import os
import shutil

def test_import_csv_success(client, app):
    source = os.path.join(os.getcwd(), 'data', 'test_meals.csv')
    dest = os.path.join(os.getcwd(), 'data', 'meals.csv')
    shutil.copy(source, dest)

    response = client.post('/meals/import_csv', json={
        "file_path": "test_meals.csv"
    })

    assert response.status_code == 201
    assert "imported successfully" in response.json["message"]
