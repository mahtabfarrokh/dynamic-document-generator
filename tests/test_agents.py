import pytest
from unittest.mock import AsyncMock, patch
from agents.general_standards_agent import generate_general_standards
from core.state import DocState
from agents.land_use_permits_agent import generate_land_use_permits
from agents.zoning_agent import generate_zoning
from core.state import DocState
import os


@pytest.fixture
def mock_state():
    return DocState()


@pytest.mark.anyio
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
@patch("litellm.acompletion")
async def test_generate_general_standards(mock_acompletion, mock_state):
    mock_response_content = '{"html_section": "<p>Test Content</p>"}'
    result = await generate_general_standards(
        mock_state,
        mock_response=mock_response_content
    )
    assert result == "<p>Test Content</p>"

@pytest.mark.anyio
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
@patch("litellm.acompletion")
async def test_generate_land_use_permits(mock_acompletion, mock_state):
    mock_response_content = '{"html_section": "<p>Land Use Permits Content</p>"}'
    result = await generate_land_use_permits(
        mock_state,
        mock_response=mock_response_content
    )
    assert result == "<p>Land Use Permits Content</p>"


@pytest.mark.anyio
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
@patch("litellm.acompletion")
async def test_generate_zoning(mock_acompletion, mock_state):
    mock_response_content = '{"html_section": "<p>Zoning Content</p>"}'
    result = await generate_zoning(
        mock_state,
        mock_response=mock_response_content
    )
    assert result == "<p>Zoning Content</p>"
