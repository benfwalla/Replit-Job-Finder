import csv
import pytest
from unittest.mock import patch, MagicMock
from main import read_existing_jobs, write_new_jobs, get_webpage_html, check_new_replit_jobs


def test_read_existing_jobs(tmpdir):
    # Create a temporary CSV file
    p = tmpdir.mkdir("sub").join("jobs.csv")
    p.write('id,title,location,url\n1,Job1,Location1,URL1\n2,Job2,Location2,URL2')

    job_ids = read_existing_jobs(p)
    assert job_ids == {'1', '2'}


def test_write_new_jobs(tmpdir):
    # Prepare new jobs data
    new_jobs = [['3', 'Job3', 'Location3', 'URL3'], ['4', 'Job4', 'Location4', 'URL4']]

    # Create a temporary CSV file
    p = tmpdir.mkdir("sub2").join("jobs.csv")
    write_new_jobs(new_jobs, p)

    # Read file and check if new jobs were added
    with open(p, 'r') as f:
        reader = csv.reader(f)
        lines = list(reader)
    assert lines == [['3', 'Job3', 'Location3', 'URL3'], ['4', 'Job4', 'Location4', 'URL4']]


@patch('main.webdriver.Chrome')
def test_get_webpage_html(mock_chrome):
    mock_chrome().page_source = '<html>Test HTML</html>'
    html = get_webpage_html('https://replit.com/site/careers')
    assert html == '<html>Test HTML</html>'


def test_check_new_replit_jobs():
    existing_job_ids = {'1', '2'}
    html = """
    <div id="open-positions">
        <div>
            <a href="/job/3">Job3</a>
            <span>Location3</span>
        </div>
        <div>
            <a href="/job/4">Job4</a>
            <span>Location4</span>
        </div>
    </div>
    """
    new_jobs = check_new_replit_jobs(existing_job_ids, html)
    assert new_jobs == [['3', 'Job3', 'Location3', '/job/3'], ['4', 'Job4', 'Location4', '/job/4']]


pytest.main()
