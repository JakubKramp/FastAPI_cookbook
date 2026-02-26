from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dri_scrapper import DRIClient
from auth.models import Profile
from auth.schemas import DietaryReferenceIntakes


@pytest.mark.asyncio
async def test_dri_scrapper(profile: Profile, dri_data: DietaryReferenceIntakes, session: AsyncSession):
    client = DRIClient()
    with patch.object(DRIClient, "extract_data", new_callable=AsyncMock) as mock_extract:
        mock_extract.return_value = dri_data
        result = await client.fill_profile(profile, session)

    assert result.calories == 2000
    assert result.carbohydrates == 250
    assert result.fat == 70
    mock_extract.assert_called_once_with(profile)

@pytest.mark.asyncio
async def test_get_age(profile):
    client = DRIClient()
    age = client.get_age(profile.age)
    assert age == '19-50 years'

@pytest.mark.asyncio
async def test_process_value_grams():
    value = "160 grams"
    client = DRIClient()
    processed_value = await client.process_value(value)
    assert processed_value == 160.0

@pytest.mark.asyncio
async def test_process_value_milligrams():
    value = "160 mg"
    client = DRIClient()
    processed_value = await client.process_value(value)
    assert processed_value == 0.160