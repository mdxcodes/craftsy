"""
Cloudinary Service Unit Tests.

Mocks the Cloudinary SDK so tests do not require real credentials.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pathlib import Path as StdPath
from unittest.mock import patch, MagicMock

import pytest

from backend.services.cloudinary_service import CloudinaryService


@pytest.fixture
def cloudinary_service():
    """Create a CloudinaryService instance with mocked config."""
    with patch("backend.services.cloudinary_service.cloudinary") as mock_cloudinary:
        with patch.object(CloudinaryService, "_configure", return_value=True):
            service = CloudinaryService.__new__(CloudinaryService)
            service.settings = MagicMock()
            service.settings.cloudinary_cloud_name = "test-cloud"
            service.settings.cloudinary_api_key = "test-key"
            service.settings.cloudinary_api_secret = "test-secret"
            service._enabled = True
            yield service


def test_upload_image_success(cloudinary_service, tmp_path):
    """Test successful image upload to Cloudinary."""
    test_file = tmp_path / "test_image.jpg"
    test_file.write_bytes(b"fake-image-data")

    mock_result = {
        "public_id": "craftsy/products/test/original",
        "secure_url": "https://res.cloudinary.com/test-cloud/image/upload/v123/craftsy/products/test/original.jpg",
        "resource_type": "image",
        "format": "jpg",
        "width": 1200,
        "height": 1200,
        "bytes": 45000,
    }

    with patch.object(cloudinary_service, "upload_image", return_value=mock_result) as mock_upload:
        result = cloudinary_service.upload_image(
            file_path=str(test_file),
            folder="craftsy/products/test",
            public_id="original",
        )
        assert result["public_id"] == "craftsy/products/test/original"
        assert result["secure_url"].startswith("https://")
        mock_upload.assert_called_once()


def test_delete_image_success(cloudinary_service):
    """Test successful image deletion from Cloudinary."""
    with patch.object(cloudinary_service, "delete_image", return_value={"result": "ok"}) as mock_delete:
        result = cloudinary_service.delete_image("craftsy/products/test/original")
        assert result["result"] == "ok"
        mock_delete.assert_called_once_with("craftsy/products/test/original")


def test_build_url(cloudinary_service):
    """Test Cloudinary URL building."""
    with patch("backend.services.cloudinary_service.cloudinary.utils.cloudinary_url") as mock_url_builder:
        mock_url_builder.return_value = "https://res.cloudinary.com/test-cloud/image/upload/w_800/craftsy/products/test/original.jpg"
        url = cloudinary_service.build_url(
            public_id="craftsy/products/test/original",
            width=800,
            crop="limit",
            quality="auto:good",
        )
        assert url.startswith("https://")
        assert "w_800" in url
        mock_url_builder.assert_called_once()


def test_extract_public_id_from_url(cloudinary_service):
    """Test extracting public ID from Cloudinary URL."""
    url = "https://res.cloudinary.com/test-cloud/image/upload/v123/craftsy/products/test/original.jpg"
    public_id = cloudinary_service.extract_public_id_from_url(url)
    assert public_id == "craftsy/products/test/original"


def test_extract_public_id_from_url_without_version(cloudinary_service):
    """Test extracting public ID from Cloudinary URL without version prefix."""
    url = "https://res.cloudinary.com/test-cloud/image/upload/craftsy/products/test/original"
    public_id = cloudinary_service.extract_public_id_from_url(url)
    assert public_id == "craftsy/products/test/original"


def test_extract_public_id_from_non_cloudinary_url(cloudinary_service):
    """Test that non-Cloudinary URLs return None."""
    url = "https://example.com/image.jpg"
    public_id = cloudinary_service.extract_public_id_from_url(url)
    assert public_id is None


def test_upload_image_not_configured():
    """Test that upload raises when Cloudinary is not configured."""
    service = CloudinaryService.__new__(CloudinaryService)
    service._enabled = False
    with pytest.raises(RuntimeError, match="Cloudinary is not configured"):
        service.upload_image(file_path="/tmp/test.jpg")


def test_upload_image_file_not_found(cloudinary_service):
    """Test that upload raises when file does not exist."""
    with pytest.raises(FileNotFoundError):
        cloudinary_service.upload_image(file_path="/tmp/nonexistent_image_xyz.jpg")


def test_delete_image_not_configured():
    """Test that delete raises when Cloudinary is not configured."""
    service = CloudinaryService.__new__(CloudinaryService)
    service._enabled = False
    with pytest.raises(RuntimeError, match="Cloudinary is not configured"):
        service.delete_image("some-public-id")


def test_delete_image_empty_public_id(cloudinary_service):
    """Test that delete raises when public_id is empty."""
    with pytest.raises(ValueError, match="public_id must not be empty"):
        cloudinary_service.delete_image("")
