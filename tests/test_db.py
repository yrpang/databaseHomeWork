import pytest
from homework.db import get_db


def test_get_close_db(app):
    with app.app_context():
        cur = get_db()
        assert cur is get_db()

    with pytest.raises(ReferenceError) as e:
        cur.execute('SELECT 1')

    assert 'weakly-referenced' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('homework.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
