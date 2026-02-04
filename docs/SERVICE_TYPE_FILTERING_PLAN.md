# Service Type Filtering Implementation Plan

## Overview
Add checkbox filters for service types (Primary Care, Dental Care, Vision, Behavioral Health) to allow users to filter health centers by the services they offer.

## Current State Analysis

### Data Structure
- CSV has multiple types columns:
  - `types` (column 8): Often empty
  - `openai_types` (column 16): Contains comma-separated service types (e.g., "Primary Care, Dental, Behavioral Health, Vision, Pharmacy")
  - `final_types` (column 25): Manually curated data (often empty)
- Service types are stored as comma-separated strings
- Examples: "Primary Care, Dental Care, Eye Care, Behavioral Health, Pharmacy"

### Frontend Usage
- `HealthCenterList.tsx`: Uses `center.types` (may be empty)
- `HealthCenterDetail.tsx`: Uses `final_types || openai_types || types` (fallback chain)
- `types.ts`: Defines `types`, `openai_types`, and `final_types` as optional strings

## Proposed Solution

### Phase 1: Data Transformation (Backend/CSV Processing)

1. **Create a Python script** to transform the CSV:
   - Parse the types column (use `openai_types` as primary source, fallback to `types` or `final_types`)
   - Normalize service type names (handle variations like "Dental" vs "Dental Care", "Eye Care" vs "Vision")
   - Create boolean columns for filtering:
     - `has_primary_care` (boolean)
     - `has_dental_care` (boolean)
     - `has_vision` (boolean)
     - `has_behavioral_health` (boolean)
   - Create `all_services` column (comma-separated string containing ALL services, including the filtered ones)
     - This field will be used for display purposes in the UI
     - Contains the complete list of services as originally provided
   - Preserve original `types` columns for backward compatibility

2. **Service Type Matching Logic**:
   - **Primary Care**: Match "primary care", "internal medicine", "family medicine", "general practice"
   - **Dental Care**: Match "dental", "dentistry", "dental care"
   - **Vision**: Match "vision", "eye care", "optometry", "ophthalmology"
   - **Behavioral Health**: Match "behavioral health", "mental health", "psychiatry", "counseling", "therapy"

3. **Output**:
   - Update `data/processed/community_health_centers_with_coords.csv`
   - Create backup before transformation
   - Update `frontend/public/data/centers.csv` (used by frontend)

### Phase 2: TypeScript Type Updates

1. **Update `types.ts`**:
   ```typescript
   export interface HealthCenter {
     // ... existing fields ...
     types: string;
     // Add new boolean fields
     has_primary_care?: boolean;
     has_dental_care?: boolean;
     has_vision?: boolean;
     has_behavioral_health?: boolean;
     other_services?: string; // comma-separated
     // ... rest of fields ...
   }
   ```

### Phase 3: Frontend Filtering UI

1. **Add filter checkboxes in `App.tsx`**:
   - Create a new filter section above the search controls
   - Add checkboxes for:
     - ☐ Primary Care
     - ☐ Dental Care
     - ☐ Vision
     - ☐ Behavioral Health
   - Style consistently with existing UI

2. **Update filtering logic in `App.tsx`**:
   - Add state for selected service type filters
   - Modify `filteredCenters` logic to:
     - First apply distance/radius filter (existing)
     - Then apply service type filters (new)
     - If no filters selected, show all centers
     - If filters selected, show centers that match ANY selected filter (OR logic)

3. **Update display components**:
   - **`HealthCenterList.tsx`**: Update to use `all_services` field
     - Fallback chain: `all_services` → `final_types` → `openai_types` → `types`
     - Display format: "Services: {all_services}"
   - **`HealthCenterDetail.tsx`**: Update `displayTypes` logic (line 24)
     - Change fallback chain to: `all_services` → `final_types` → `openai_types` → `types`
     - This ensures consistent display across both components

### Phase 4: CSV Loader Updates

1. **Update `csvLoader.ts`**:
   - Parse boolean columns (`has_primary_care`, etc.) as booleans
   - Handle missing values gracefully (default to false)

### Phase 5: OpenAI Enrichment Updates

1. **Create utility function for type parsing**:
   - Create `scripts/utils/parse_service_types.py` (or similar)
   - Function: `parse_service_types(types_string: str) -> dict`
   - Returns dictionary with:
     - `has_primary_care`: boolean
     - `has_dental_care`: boolean
     - `has_vision`: boolean
     - `has_behavioral_health`: boolean
     - `all_services`: string (normalized, comma-separated)
   - Uses same matching logic as Phase 1 transformation script

2. **Update backend enrichment endpoint** (if exists):
   - **File**: `backend/app/services/openai_enrichment.py` (or create if needed)
   - **Endpoint**: `POST /api/enrich-center`
   - After receiving `openai_types` from OpenAI API:
     - Call `parse_service_types()` utility function
     - Add boolean fields to response:
       - `openai_has_primary_care`
       - `openai_has_dental_care`
       - `openai_has_vision`
       - `openai_has_behavioral_health`
     - Add `openai_all_services` field (normalized version of `openai_types`)
   - Response now includes both:
     - Original `openai_types` (for backward compatibility)
     - New boolean fields (for filtering)
     - New `openai_all_services` (for display)

3. **Update enrichment script**:
   - **File**: `scripts/enrich_csv.py`
   - Add new columns to `OPENAI_COLUMNS`:
     - `openai_has_primary_care`
     - `openai_has_dental_care`
     - `openai_has_vision`
     - `openai_has_behavioral_health`
     - `openai_all_services`
   - Import and use the `parse_service_types()` utility function
   - When processing API response, populate boolean fields from `openai_types`

4. **Update CSV schema documentation**:
   - Document new OpenAI enrichment columns
   - Explain that boolean fields are auto-populated from `openai_types`

## Implementation Steps

1. ✅ Create branch: `feature/service-type-filtering`
2. ⏳ Create Python script to transform CSV
3. ⏳ Run transformation script and verify output
4. ⏳ Create utility function for type parsing (reusable for enrichment)
5. ⏳ Update TypeScript types
6. ⏳ Update CSV loader to parse boolean fields
7. ⏳ Update OpenAI enrichment endpoint/script to populate new fields
8. ⏳ Add filter UI components
9. ⏳ Implement filtering logic
10. ⏳ Update display components
11. ⏳ Test with various filter combinations
12. ⏳ Update documentation

## Edge Cases to Handle

1. **Empty types**: If all types columns are empty, all booleans = false, all_services = ""
2. **Case sensitivity**: Normalize to lowercase for matching
3. **Variations**: Handle "Dental" vs "Dental Care", "Eye Care" vs "Vision"
4. **Multiple matches**: A center can have multiple service types
5. **Backward compatibility**: Keep original `types` columns for fallback

## Testing Considerations

1. Test with centers that have:
   - All four service types
   - Only one service type
   - No matching service types (should go to "other")
   - Empty types data
2. Test filter combinations:
   - Single filter selected
   - Multiple filters selected (OR logic)
   - No filters selected (show all)
3. Test with distance filtering combined with service type filtering

## Alternative Approaches Considered

1. **Keep types as string, parse on frontend**: 
   - ❌ Less efficient, harder to query
   - ❌ Requires parsing on every filter change

2. **Use separate CSV with normalized types**:
   - ❌ Adds complexity, need to join data
   - ❌ More files to maintain

3. **Use database instead of CSV**:
   - ❌ Overkill for current scale
   - ❌ Requires infrastructure changes

## Recommendation

**Proceed with Phase 1-4 approach**: Transform CSV to add boolean columns for filtering and `all_services` for display, update frontend to use them. This provides:
- ✅ Efficient filtering using boolean columns
- ✅ Easy display using `all_services` field (no need to reconstruct from booleans)
- ✅ Clear data structure
- ✅ Easy to extend with more service types
- ✅ Maintains backward compatibility

## Data Structure Summary

- **Boolean columns** (`has_primary_care`, `has_dental_care`, `has_vision`, `has_behavioral_health`): Used for filtering
- **`all_services` column**: Contains complete comma-separated list of all services for display
- **Original columns** (`types`, `openai_types`, `final_types`): Preserved for backward compatibility

### OpenAI Enrichment Columns (Future)

When OpenAI enrichment is called, it will populate:
- `openai_types`: Original comma-separated string (backward compatible)
- `openai_has_primary_care`, `openai_has_dental_care`, `openai_has_vision`, `openai_has_behavioral_health`: Boolean fields
- `openai_all_services`: Normalized comma-separated string for display

The enrichment process will automatically parse `openai_types` and populate the boolean fields and `all_services` field, so future enrichment calls will directly fill in the CSV with the correct structure.
