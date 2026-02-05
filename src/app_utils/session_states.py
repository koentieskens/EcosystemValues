
import streamlit as st
from functools import wraps


class SessionStateVariable:
    """Individual session state variable with its own methods"""

    def __init__(self, key: str, default_value):
        self.key = key
        self.default_value = default_value

    def __repr__(self):
        return f"SessionStateVariable('{self.key}', {self.get()})"

    def __eq__(self, other):
        """Allow direct comparison: if SessionStateManager.ZOOM_LEVEL == 5:"""
        return self.get() == other

    def __bool__(self):
        """Allow direct boolean usage: if SessionStateManager.INIT_DONE:"""
        return bool(self.get())

    def initialize(self):
        """Initialize this variable in session state if not present"""
        if self.key not in st.session_state:
            st.session_state[self.key] = self.default_value

    def get(self):
        """Get the current value from session state"""
        return st.session_state.get(self.key, self.default_value)

    def set(self, value):
        """Set the value in session state"""
        st.session_state[self.key] = value

    def reset(self):
        """Reset to default value"""
        st.session_state[self.key] = self.default_value

    def is_true(self):
        """Check if value is True (useful for boolean flags)"""
        return self.get() is True

    def is_false(self):
        """Check if value is False"""
        return self.get() is False

    def is_none(self):
        """Check if value is None"""
        return self.get() is None

    def skip_if_true(self):
        """Decorator that skips function execution if this variable is True"""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if self.is_true():
                    return
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def skip_if_false(self):
        """Decorator that skips function execution if this variable is False"""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if self.is_false():
                    return
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def skip_if_none(self):
        """Decorator that skips function execution if this variable is None"""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if self.is_none():
                    return
                return func(*args, **kwargs)

            return wrapper

        return decorator


class SessionStateManager:
    """Manager for all session state variables"""

    # Create SessionStateVariable instances
    INIT_DONE = SessionStateVariable('init_done', False)
    MODEL_CLASS = SessionStateVariable('model_class', None)
    PREDICTION_SETS = SessionStateVariable('prediction_sets', {})
    SIIKAMAKI_BENEFITS = SessionStateVariable('siikamaki_benefits', None)
    CACHED_MAP = SessionStateVariable('cached_map', None)
    ZOOM_LEVEL = SessionStateVariable('zoom_level', 2)
    ECOSYSTEM_TYPE = SessionStateVariable('ecosystem_type', None)
    GEE_INITIALIZED = SessionStateVariable('gee_initialized', False)
    INSTANTIATED = SessionStateVariable('instantiated', False)
    SELECTED_BIOME = SessionStateVariable('selected_biome', None)
    SELECTED_SUB_BIOME = SessionStateVariable('selected_sub_biome', None)
    ECOSYSTEM_DISPLAY_NAME = SessionStateVariable('ecosystem_display_name', None)
    SPATIAL_VARIABLES = SessionStateVariable('spatial_variables', {})
    BENEFITS_UPDATED = SessionStateVariable('benefits_updated', False)

    LOCATION_ACTIVATED = SessionStateVariable('location_activated', False)
    LOCATION_TYPE = SessionStateVariable('location_type', 'manual')
    UNSAVED_POLYGON = SessionStateVariable('unsaved_polygon', None)
    DRAWN_POLYGON = SessionStateVariable('drawn_polygon', None)
    SAVED_POLYGON = SessionStateVariable('saved_polygon', None)
    MANUAL_CENTROID = SessionStateVariable('manual_centroid', (40.0, 10.0))
    MANUAL_AREA = SessionStateVariable('manual_area', 1.0)
    TEMP_MANUAL_POLYGON = SessionStateVariable('temp_manual_polygon', None)
    MANUAL_POLYGON = SessionStateVariable('manual_polygon', None)
    POLYGON_CENTROID = SessionStateVariable('polygon_centroid', (40.0, 10.0))
    POLYGON_AREA = SessionStateVariable('polygon_area', 1.0)
    AOI_GDF = SessionStateVariable('aoi_gdf', None)
    PROJECT_LOCATION = SessionStateVariable('project_location', {'lat': 40.0, 'lon': 10.0, 'area': 1.0})
    ECOSYSTEM_SERVICES = SessionStateVariable('ecosystem_services', [])
    COST_CALCULATIONS = SessionStateVariable('cost_calculations', None)
    COST_UPDATED = SessionStateVariable('cost_updated', False)
    FORM_SUBMITTED = SessionStateVariable('form_submitted', False)
    COST_UPDATE_FROM_EXTRACTION = SessionStateVariable('cost_update_from_extraction', False)
    COST_EXTRACTION_DONE = SessionStateVariable('cost_extraction_done', False)
    COST_EXTRACTED_VALUES = SessionStateVariable('cost_extracted_values', {})
    BENEFITS_UPDATE_FROM_EXTRACTION = SessionStateVariable('benefits_update_from_extraction', False)
    BENEFITS_EXTRACTION_DONE = SessionStateVariable('benefits_extraction_done', False)
    BENEFITS_EXTRACTED_VALUES = SessionStateVariable('benefits_extracted_values', {})
    DISPLAYED_COST = SessionStateVariable('displayed_cost', False)
    DISPLAYED_BENEFITS = SessionStateVariable('displayed_benefits', False)
    COST_DATA = SessionStateVariable('cost_data', None)
    SAVED_COUNTRY = SessionStateVariable('saved_country', None)
    SAVED_REGION = SessionStateVariable('saved_region', None)

    @classmethod
    def get_all_variables(cls):
        """Automatically collect all SessionStateVariable instances"""
        return [getattr(cls, attr) for attr in dir(cls)
                if isinstance(getattr(cls, attr), SessionStateVariable)]

    @classmethod
    def initialize_all(cls):
        """Initialize all session state variables"""
        for variable in cls.get_all_variables():
            variable.initialize()

    @classmethod
    def reset_all(cls):
        """Reset all variables to their default values"""
        for variable in cls.get_all_variables():
            variable.reset()




