#!/usr/bin/env python3
"""
Setup script for Supabase database schema
Run this after creating your Supabase project to set up the required tables.
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def get_supabase_client() -> Client:
    """Get Supabase client from environment variables"""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    
    return create_client(supabase_url, supabase_key)

def create_tables():
    """Create the required tables in Supabase"""
    print("Setting up Supabase database schema...")
    
    # SQL commands to create tables
    sql_commands = [
        # Create operators table
        """
        CREATE TABLE IF NOT EXISTS operators (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name TEXT NOT NULL,
            organization_type TEXT,
            contact_info JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """,
        
        # Create climate_grid_cells table
        """
        CREATE TABLE IF NOT EXISTS climate_grid_cells (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            cell_id TEXT UNIQUE NOT NULL,
            latitude_min DOUBLE PRECISION NOT NULL,
            latitude_max DOUBLE PRECISION NOT NULL,
            longitude_min DOUBLE PRECISION NOT NULL,
            longitude_max DOUBLE PRECISION NOT NULL,
            center_latitude DOUBLE PRECISION NOT NULL,
            center_longitude DOUBLE PRECISION NOT NULL,
            region_name TEXT,
            climate_zone TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """,
        
        # Create interventions table
        """
        CREATE TABLE IF NOT EXISTS interventions (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            operator_id UUID NOT NULL REFERENCES operators(id),
            grid_cell_id UUID NOT NULL REFERENCES climate_grid_cells(id),
            name TEXT NOT NULL,
            description TEXT,
            intervention_type TEXT NOT NULL,
            status TEXT NOT NULL,
            latitude DOUBLE PRECISION NOT NULL,
            longitude DOUBLE PRECISION NOT NULL,
            region_name TEXT,
            scale_amount DOUBLE PRECISION NOT NULL,
            scale_unit TEXT NOT NULL,
            cost_usd DOUBLE PRECISION,
            start_date DATE,
            end_date DATE,
            duration_months INTEGER,
            deployment_data JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """,
        
        # Create indexes for performance
        """
        CREATE INDEX IF NOT EXISTS idx_interventions_geospatial ON interventions(latitude, longitude);
        CREATE INDEX IF NOT EXISTS idx_interventions_operator ON interventions(operator_id);
        CREATE INDEX IF NOT EXISTS idx_interventions_grid_cell ON interventions(grid_cell_id);
        CREATE INDEX IF NOT EXISTS idx_interventions_type ON interventions(intervention_type);
        CREATE INDEX IF NOT EXISTS idx_interventions_status ON interventions(status);
        CREATE INDEX IF NOT EXISTS idx_interventions_timeline ON interventions(start_date, end_date);
        """,
        
        # Create data_sources table
        """
        CREATE TABLE IF NOT EXISTS data_sources (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name TEXT NOT NULL,
            description TEXT,
            source_type TEXT NOT NULL,
            url TEXT,
            api_endpoint TEXT,
            credentials JSONB,
            update_frequency TEXT,
            last_updated TIMESTAMP WITH TIME ZONE,
            is_active BOOLEAN DEFAULT TRUE,
            metadata JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """,
        
        # Create satellite_data table
        """
        CREATE TABLE IF NOT EXISTS satellite_data (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            data_source_id UUID REFERENCES data_sources(id),
            grid_cell_id UUID REFERENCES climate_grid_cells(id),
            timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
            data_type TEXT NOT NULL,
            value DOUBLE PRECISION NOT NULL,
            unit TEXT NOT NULL,
            confidence_score DOUBLE PRECISION,
            raw_data JSONB,
            processed_data JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """,
        
        # Create intervention_impacts table
        """
        CREATE TABLE IF NOT EXISTS intervention_impacts (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            intervention_id UUID NOT NULL REFERENCES interventions(id),
            impact_type TEXT NOT NULL,
            metric_name TEXT NOT NULL,
            value_before DOUBLE PRECISION,
            value_after DOUBLE PRECISION,
            change_amount DOUBLE PRECISION,
            change_percentage DOUBLE PRECISION,
            measurement_date DATE NOT NULL,
            confidence_level DOUBLE PRECISION,
            methodology TEXT,
            verification_status TEXT,
            notes TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """,
        
        # Create optimization_results table
        """
        CREATE TABLE IF NOT EXISTS optimization_results (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            optimization_name TEXT NOT NULL,
            objective_function TEXT NOT NULL,
            constraints JSONB,
            parameters JSONB,
            results JSONB NOT NULL,
            performance_metrics JSONB,
            execution_time_seconds DOUBLE PRECISION,
            convergence_status TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
    ]
    
    try:
        supabase = get_supabase_client()
        
        for i, sql in enumerate(sql_commands, 1):
            print(f"Executing command {i}/{len(sql_commands)}...")
            result = supabase.rpc('exec_sql', {'sql': sql}).execute()
            print(f"✓ Command {i} completed")
        
        print("\n✅ Database schema setup completed successfully!")
        print("\nNext steps:")
        print("1. Set up Row Level Security (RLS) policies if needed")
        print("2. Create test data using the API endpoints")
        print("3. Run the test suite to verify everything works")
        
    except Exception as e:
        print(f"❌ Error setting up database schema: {e}")
        print("\nNote: You may need to run these SQL commands manually in the Supabase SQL editor:")
        for i, sql in enumerate(sql_commands, 1):
            print(f"\n--- Command {i} ---")
            print(sql.strip())

if __name__ == "__main__":
    create_tables() 