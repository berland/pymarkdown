"""
Module to provide tests related to the MD042 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md042_good_non_empty_link():
    """
    Test to make sure this rule does not trigger with a document that
    contains links that have non-empty urls.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md042/good_non_empty_link.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md042_bad_empty_link():
    """
    Test to make sure this rule does trigger with a document that
    contains links that have empty urls.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md042/bad_empty_link.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md042/bad_empty_link.md:2:1: "
        + "MD042: No empty links (no-empty-links)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md042_bad_whitespace_link():
    """
    Test to make sure this rule does trigger with a document that
    contains links that have whitespace only urls.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md042/bad_whitespace_link.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md042/bad_whitespace_link.md:2:1: "
        + "MD042: No empty links (no-empty-links)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md042_good_non_empty_fragment():
    """
    Test to make sure this rule does not trigger with a document that
    contains links that has a non-empty url fragment.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md042/good_non_empty_fragment.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md042_bad_link_empty_fragment():
    """
    Test to make sure this rule does trigger with a document that
    contains links that have empty url fragments.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md042/bad_link_empty_fragment.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md042/bad_link_empty_fragment.md:2:1: "
        + "MD042: No empty links (no-empty-links)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md042_bad_link_whitespace_fragment():
    """
    Test to make sure this rule does trigger with a document that
    contains links that have whitespace only url fragments.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md042/bad_link_whitespace_fragment.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md042/bad_link_whitespace_fragment.md:2:1: "
        + "MD042: No empty links (no-empty-links)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md042_good_non_empty_image():
    """
    Test to make sure this rule does not trigger with a document that
    contains images that have non-empty urls.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md042/good_non_empty_image.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md042_bad_empty_image():
    """
    Test to make sure this rule does trigger with a document that
    contains links that have empty urls.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md042/bad_empty_image.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md042/bad_empty_image.md:2:1: "
        + "MD042: No empty links (no-empty-links)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
