# Community Health Center Search Roadmap

## ✅ Completed

### Phase 1: Foundation & Infrastructure
- [x] Set up repository structure (scripts/, data/, docs/, reports/)
- [x] Initialize frontend (Vite + React 19 + TypeScript)
- [x] Initialize backend (FastAPI)
- [x] Create interactive map with Leaflet/OpenStreetMap (free, no API key)
- [x] Implement zipcode search functionality
- [x] Add distance calculation and filtering
- [x] Create health center list and detail views
- [x] Set up GitHub Pages deployment with GitHub Actions

### Phase 2: Data Pipeline
- [x] Document parser (`scripts/scrape_docx.py`) - extracts data from official Word documents
- [x] Geocoding script (`scripts/add_geocoding.py`) - adds coordinates to addresses
- [x] Data organization (raw/processed CSV files)
- [x] Removed redundant data files

### Phase 3: Data Enrichment
- [x] OpenAI enrichment pipeline (`scripts/enrich_csv.py`)
- [x] Backend API endpoint for enrichment (`/api/enrich-center`)
- [x] Comparison report generation for manual review
- [x] Frontend display of enriched data (new patient instructions, verified info)

### Phase 4: Documentation
- [x] Comprehensive documentation in `docs/` folder
- [x] Maps setup guide (Leaflet/OpenStreetMap)
- [x] Data onboarding guide
- [x] Deployment guide
- [x] OpenAI enrichment documentation
- [x] Repository organization guide

---

## 🚧 In Progress / Next Steps

### Phase 5: VAPI Integration & Call Data Collection

#### 5.1 Update VAPI to Call All Health Centers
- [ ] **Batch calling system**
  - [ ] Update `vapi/vapi_call_manager.py` to process all health centers from CSV
  - [ ] Add rate limiting and error handling for bulk calls
  - [ ] Implement retry logic for failed calls
  - [ ] Add progress tracking and reporting

- [ ] **Call data collection**
  - [ ] Collect call results: accepting new patients, waiting lists, languages supported
  - [ ] Save call transcripts and notes
  - [ ] Track call status (completed, failed, no answer, etc.)
  - [ ] Store call timestamps and metadata

#### 5.2 Update CSV with Call Results
- [ ] **Add/update call data columns**
  - [ ] Use `vapi/add_call_fields_to_csv.py` to add call fields if not present
  - [ ] Update `data/processed/community_health_centers_with_coords.csv` with VAPI call results
  - [ ] Merge call data with existing enrichment data
  - [ ] Create `final_*` columns combining OpenAI enrichment + VAPI call data

- [ ] **Data quality**
  - [ ] Resolve conflicts between OpenAI enrichment and VAPI call data
  - [ ] Prioritize VAPI call data (most recent/accurate) for final columns
  - [ ] Update `final_phone`, `final_address`, `final_new_patient_md` based on call results

#### 5.3 Frontend Integration
- [ ] **Display call data on website**
  - [ ] Update `frontend/src/types.ts` to include VAPI call fields
  - [ ] Update `frontend/src/components/HealthCenterDetail.tsx` to show:
    - [ ] Accepting new patients status
    - [ ] Waiting list information
    - [ ] Languages supported
    - [ ] Last called date
  - [ ] Prioritize `final_*` columns over `openai_*` columns
  - [ ] Show call status indicators (verified via call, last updated, etc.)

- [ ] **Data refresh**
  - [ ] Copy updated CSV to `frontend/public/data/centers.csv`
  - [ ] Test display of call data in detail view
  - [ ] Update map/list views if needed

### Phase 6: User Analytics & Booking Tracking

#### 6.1 Booking Questionnaire
- [ ] **Add questionnaire component**
  - [ ] Create questionnaire modal/form after user views health center details
  - [ ] Questions to include:
    - [ ] Did you book an appointment? (Yes/No)
    - [ ] Which health center did you contact?
    - [ ] How did you contact them? (Phone/Website/In-person)
    - [ ] Was the information helpful? (Rating 1-5)
    - [ ] Any additional feedback? (Optional text)
  - [ ] Show questionnaire after user clicks "Get Directions" or views contact info
  - [ ] Make it optional but visible

- [ ] **Questionnaire UI**
  - [ ] Design user-friendly questionnaire component
  - [ ] Add to `frontend/src/components/`
  - [ ] Integrate with existing detail view
  - [ ] Store responses locally (localStorage) before submission
  - [ ] Add "Skip" option

#### 6.2 Analytics Backend
- [ ] **Create analytics API endpoint**
  - [ ] Add endpoint: `POST /api/analytics/booking`
  - [ ] Store booking data in database or file
  - [ ] Track metrics:
    - [ ] Number of bookings per health center
    - [ ] Booking method (phone/website/in-person)
    - [ ] User satisfaction ratings
    - [ ] Health centers most frequently contacted
    - [ ] Conversion rate (views → bookings)

- [ ] **Data storage**
  - [ ] Choose storage solution:
    - [ ] Option A: JSON file (`data/analytics/bookings.json`)
    - [ ] Option B: SQLite database (`data/analytics/analytics.db`)
    - [ ] Option C: Backend database (PostgreSQL/MongoDB)
  - [ ] Create analytics data structure
  - [ ] Implement data aggregation functions

#### 6.3 Analytics Dashboard (Optional)
- [ ] **Admin dashboard**
  - [ ] Create analytics dashboard page
  - [ ] Display booking statistics
  - [ ] Show health center performance metrics
  - [ ] Export analytics data (CSV/JSON)
  - [ ] Visualizations (charts/graphs)

---

## 🔮 Future Enhancements

### Phase 7: Enhanced Features
- [ ] Real-time availability updates
- [ ] Appointment booking integration
- [ ] Calendar integration (Google Calendar, Outlook)
- [ ] SMS/email notifications
- [ ] Advanced search filters (insurance, services, languages)
- [ ] Provider reviews and ratings system
- [ ] Multi-language support

### Phase 8: Mobile & Expansion
- [ ] Mobile app development (React Native)
- [ ] Integration with healthcare systems (EHR)
- [ ] Telemedicine platform integration
- [ ] Multi-region expansion (beyond Massachusetts)
- [ ] Provider network partnerships

---

## 📊 Current Status Summary

**Completed:** Foundation, data pipeline, enrichment, documentation, deployment  
**In Progress:** VAPI integration for bulk calling  
**Next:** Call data integration, frontend updates, analytics  

**Key Metrics to Track:**
- Number of health centers called via VAPI
- Call success rate
- Booking conversion rate
- User satisfaction scores
- Most contacted health centers

---

## 🎯 Immediate Priorities

1. **VAPI Bulk Calling** - Call all health centers and collect data
2. **Data Integration** - Update CSV with call results and create final columns
3. **Frontend Updates** - Display call data on website
4. **Analytics Setup** - Implement questionnaire and data collection
5. **Analytics Storage** - Save and aggregate booking data

---

*Last updated: January 2025*
