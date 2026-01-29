import pytest
import os
import Mini_Project_1 as mp1
from unittest.mock import patch, MagicMock


def test_tc1_valid_markdown_file(tmp_path):
    file = tmp_path / "test.md"
    file.write_text("# Hello World")
    assert mp1.is_markdown_file(str(file)) is True

def test_tc2_non_markdown_file():
    assert mp1.is_markdown_file("test.txt") is False

def test_tc3_empty_markdown_file(tmp_path):
    file = tmp_path / "empty.md"
    file.write_text("")
    content = file.read_text()
    assert mp1.count_words(content) == 0
    assert sum(mp1.count_headings(content).values()) == 0

def test_tc4_file_not_found():
    assert not os.path.exists("no_such_file.md")


def test_tc5_simple_word_count():
    content = "Hello world"
    assert mp1.count_words(content) == 2

def test_tc7_multiline_word_count():
    content = "Hello world\nThis is markdown"
    assert mp1.count_words(content) == 5


def test_tc8_single_heading():
    content = "# Heading"
    headings = mp1.count_headings(content)
    assert headings["h1"] == 1

def test_tc9_multiple_headings():
    content = "# H1\n## H2\n### H3"
    headings = mp1.count_headings(content)
    assert headings["h1"] == 1
    assert headings["h2"] == 1
    assert headings["h3"] == 1

def test_tc10_no_headings():
    content = "Just plain text"
    headings = mp1.count_headings(content)
    assert sum(headings.values()) == 0


def test_tc11_single_link():
    content = "[Google](https://google.com)"
    links = mp1.extract_links(content)
    assert len(links) == 1

def test_tc12_multiple_links():
    content = "[A](https://a.com)\n[B](https://b.com)"
    links = mp1.extract_links(content)
    assert len(links) == 2

def test_tc14_relative_link():
    content = "[Readme](README.md)"
    links = mp1.extract_links(content)
    assert len(links) == 1
    # Check the URL field in the dictionary
    assert links[0]['url'] == "README.md"


def test_tc15_single_image():
    content = "![Logo](logo.png)"
    images = mp1.extract_images(content)
    assert len(images) == 1

def test_tc16_multiple_images():
    content = "![A](a.png)\n![B](b.jpg)"
    images = mp1.extract_images(content)
    assert len(images) == 2

def test_tc17_broken_image_still_counted():
    content = "![Broken](missing.png)"
    images = mp1.extract_images(content)
    assert len(images) == 1


@patch("Mini_Project_1.requests.head")
def test_tc13_broken_link(mock_head):
    mock_head.side_effect = Exception("Connection error")
    
    # Create links in the format expected by validate_links
    links = [{'text': 'Broken', 'url': 'https://broken-link.com', 'type': 'standard'}]
    
    # Create a minimal config
    config = {'timeout': 5}
    
    broken = mp1.validate_links(links, config)
    assert len(broken) == 1

@patch("Mini_Project_1.requests.head")
def test_tc21_no_internet(mock_head):
    mock_head.side_effect = Exception("No internet")
    
    # Create links in the format expected by validate_links
    links = [{'text': 'Google', 'url': 'https://google.com', 'type': 'standard'}]
    
    # Create a minimal config
    config = {'timeout': 5}
    
    broken = mp1.validate_links(links, config)
    assert len(broken) == 1


def test_tc20_large_markdown_file():
   
    content = "# Title\n" + ("word " * 5000)
    count = mp1.count_words(content)
    
    assert count == 5001