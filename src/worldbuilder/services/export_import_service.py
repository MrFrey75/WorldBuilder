"""Export and Import service for universe data management."""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from worldbuilder.models import (
    Universe, Location, Species, NotableFigure, 
    Relationship, Event, Organization, Artifact, Lore
)


class ExportImportService:
    """Service for exporting and importing universe data."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def export_universe(self, universe_id: int, output_path: str, 
                       selective: bool = False, entity_types: List[str] = None) -> Dict[str, Any]:
        """Export a complete universe or selective entities to JSON.
        
        Args:
            universe_id: ID of universe to export
            output_path: Path to output JSON file
            selective: If True, only export specified entity types
            entity_types: List of entity types to export (if selective=True)
                         Options: 'locations', 'species', 'figures', 'relationships', 
                         'events', 'organizations', 'artifacts', 'lore'
        
        Returns:
            Dictionary with export statistics
        
        Raises:
            ValueError: If universe not found
        """
        universe = self.session.query(Universe).filter_by(id=universe_id).first()
        if not universe:
            raise ValueError(f"Universe with ID {universe_id} not found")
        
        # Prepare export data structure
        export_data = {
            "export_metadata": {
                "version": "1.0",
                "export_date": datetime.now().isoformat(),
                "universe_id": universe_id,
                "universe_name": universe.name
            },
            "universe": self._serialize_entity(universe),
            "data": {}
        }
        
        # Define entity types to export
        if selective and entity_types:
            types_to_export = entity_types
        else:
            types_to_export = ['locations', 'species', 'figures', 'relationships', 
                             'events', 'organizations', 'artifacts', 'lore']
        
        stats = {"total_entities": 0}
        
        # Export each entity type
        if 'locations' in types_to_export:
            locations = self.session.query(Location).filter_by(universe_id=universe_id).all()
            export_data["data"]["locations"] = [self._serialize_entity(loc) for loc in locations]
            stats["locations"] = len(locations)
            stats["total_entities"] += len(locations)
        
        if 'species' in types_to_export:
            species = self.session.query(Species).filter_by(universe_id=universe_id).all()
            export_data["data"]["species"] = [self._serialize_entity(sp) for sp in species]
            stats["species"] = len(species)
            stats["total_entities"] += len(species)
        
        if 'figures' in types_to_export:
            figures = self.session.query(NotableFigure).filter_by(universe_id=universe_id).all()
            export_data["data"]["figures"] = [self._serialize_entity(fig) for fig in figures]
            stats["figures"] = len(figures)
            stats["total_entities"] += len(figures)
        
        if 'relationships' in types_to_export:
            relationships = self.session.query(Relationship).filter_by(universe_id=universe_id).all()
            export_data["data"]["relationships"] = [self._serialize_entity(rel) for rel in relationships]
            stats["relationships"] = len(relationships)
            stats["total_entities"] += len(relationships)
        
        if 'events' in types_to_export:
            events = self.session.query(Event).filter_by(universe_id=universe_id).all()
            export_data["data"]["events"] = [self._serialize_entity(evt) for evt in events]
            stats["events"] = len(events)
            stats["total_entities"] += len(events)
        
        if 'organizations' in types_to_export:
            organizations = self.session.query(Organization).filter_by(universe_id=universe_id).all()
            export_data["data"]["organizations"] = [self._serialize_entity(org) for org in organizations]
            stats["organizations"] = len(organizations)
            stats["total_entities"] += len(organizations)
        
        if 'artifacts' in types_to_export:
            artifacts = self.session.query(Artifact).filter_by(universe_id=universe_id).all()
            export_data["data"]["artifacts"] = [self._serialize_entity(art) for art in artifacts]
            stats["artifacts"] = len(artifacts)
            stats["total_entities"] += len(artifacts)
        
        if 'lore' in types_to_export:
            lore_items = self.session.query(Lore).filter_by(universe_id=universe_id).all()
            export_data["data"]["lore"] = [self._serialize_entity(lore) for lore in lore_items]
            stats["lore"] = len(lore_items)
            stats["total_entities"] += len(lore_items)
        
        # Write to file
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        stats["output_file"] = output_path
        stats["file_size"] = os.path.getsize(output_path)
        
        return stats
    
    def import_universe(self, input_path: str, create_new: bool = True, 
                       target_universe_id: Optional[int] = None) -> Dict[str, Any]:
        """Import universe data from JSON file.
        
        Args:
            input_path: Path to JSON export file
            create_new: If True, create a new universe. If False, import into existing
            target_universe_id: ID of target universe (required if create_new=False)
        
        Returns:
            Dictionary with import statistics
        
        Raises:
            ValueError: If file not found or invalid data
        """
        if not os.path.exists(input_path):
            raise ValueError(f"Import file not found: {input_path}")
        
        # Read import file
        with open(input_path, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        # Validate import data
        if "export_metadata" not in import_data or "universe" not in import_data:
            raise ValueError("Invalid import file format")
        
        stats = {"total_entities": 0, "skipped": 0, "errors": []}
        
        # Create or get target universe
        if create_new:
            universe_data = import_data["universe"]
            universe = Universe(
                name=universe_data["name"] + " (Imported)",
                description=universe_data.get("description"),
                author=universe_data.get("author"),
                genre=universe_data.get("genre"),
                is_active=False
            )
            self.session.add(universe)
            self.session.flush()
            target_universe_id = universe.id
            stats["new_universe_id"] = target_universe_id
        else:
            if not target_universe_id:
                raise ValueError("target_universe_id required when create_new=False")
            universe = self.session.query(Universe).filter_by(id=target_universe_id).first()
            if not universe:
                raise ValueError(f"Target universe {target_universe_id} not found")
        
        data = import_data.get("data", {})
        
        # ID mapping for maintaining relationships
        id_mapping = {
            'locations': {},
            'species': {},
            'figures': {},
            'events': {},
            'organizations': {},
            'artifacts': {},
            'lore': {}
        }
        
        # Import entities in dependency order
        
        # 1. Locations (handle parent relationships later)
        if 'locations' in data:
            for loc_data in data['locations']:
                try:
                    old_id = loc_data.pop('id')
                    loc_data.pop('created_at', None)
                    loc_data.pop('updated_at', None)
                    loc_data['universe_id'] = target_universe_id
                    loc_data['parent_id'] = None  # Will be set later
                    
                    location = Location(**loc_data)
                    self.session.add(location)
                    self.session.flush()
                    id_mapping['locations'][old_id] = location.id
                    stats["total_entities"] += 1
                except Exception as e:
                    stats["errors"].append(f"Location import error: {str(e)}")
                    stats["skipped"] += 1
        
        # Update location parent relationships
        if 'locations' in data:
            for loc_data in data['locations']:
                if loc_data.get('parent_id'):
                    old_parent_id = loc_data['parent_id']
                    if old_parent_id in id_mapping['locations']:
                        new_id = id_mapping['locations'][loc_data['id']]
                        location = self.session.query(Location).filter_by(id=new_id).first()
                        if location:
                            location.parent_id = id_mapping['locations'][old_parent_id]
        
        # 2. Species
        if 'species' in data:
            for sp_data in data['species']:
                try:
                    old_id = sp_data.pop('id')
                    sp_data.pop('created_at', None)
                    sp_data.pop('updated_at', None)
                    sp_data['universe_id'] = target_universe_id
                    
                    species = Species(**sp_data)
                    self.session.add(species)
                    self.session.flush()
                    id_mapping['species'][old_id] = species.id
                    stats["total_entities"] += 1
                except Exception as e:
                    stats["errors"].append(f"Species import error: {str(e)}")
                    stats["skipped"] += 1
        
        # 3. Figures
        if 'figures' in data:
            for fig_data in data['figures']:
                try:
                    old_id = fig_data.pop('id')
                    fig_data.pop('created_at', None)
                    fig_data.pop('updated_at', None)
                    fig_data['universe_id'] = target_universe_id
                    
                    # Update foreign key references
                    if fig_data.get('species_id') and fig_data['species_id'] in id_mapping['species']:
                        fig_data['species_id'] = id_mapping['species'][fig_data['species_id']]
                    
                    figure = NotableFigure(**fig_data)
                    self.session.add(figure)
                    self.session.flush()
                    id_mapping['figures'][old_id] = figure.id
                    stats["total_entities"] += 1
                except Exception as e:
                    stats["errors"].append(f"Figure import error: {str(e)}")
                    stats["skipped"] += 1
        
        # 4. Organizations
        if 'organizations' in data:
            for org_data in data['organizations']:
                try:
                    old_id = org_data.pop('id')
                    org_data.pop('created_at', None)
                    org_data.pop('updated_at', None)
                    org_data['universe_id'] = target_universe_id
                    
                    organization = Organization(**org_data)
                    self.session.add(organization)
                    self.session.flush()
                    id_mapping['organizations'][old_id] = organization.id
                    stats["total_entities"] += 1
                except Exception as e:
                    stats["errors"].append(f"Organization import error: {str(e)}")
                    stats["skipped"] += 1
        
        # 5. Events
        if 'events' in data:
            for evt_data in data['events']:
                try:
                    old_id = evt_data.pop('id')
                    evt_data.pop('created_at', None)
                    evt_data.pop('updated_at', None)
                    evt_data['universe_id'] = target_universe_id
                    
                    event = Event(**evt_data)
                    self.session.add(event)
                    self.session.flush()
                    id_mapping['events'][old_id] = event.id
                    stats["total_entities"] += 1
                except Exception as e:
                    stats["errors"].append(f"Event import error: {str(e)}")
                    stats["skipped"] += 1
        
        # 6. Artifacts
        if 'artifacts' in data:
            for art_data in data['artifacts']:
                try:
                    old_id = art_data.pop('id')
                    art_data.pop('created_at', None)
                    art_data.pop('updated_at', None)
                    art_data['universe_id'] = target_universe_id
                    
                    artifact = Artifact(**art_data)
                    self.session.add(artifact)
                    self.session.flush()
                    id_mapping['artifacts'][old_id] = artifact.id
                    stats["total_entities"] += 1
                except Exception as e:
                    stats["errors"].append(f"Artifact import error: {str(e)}")
                    stats["skipped"] += 1
        
        # 7. Lore
        if 'lore' in data:
            for lore_data in data['lore']:
                try:
                    old_id = lore_data.pop('id')
                    lore_data.pop('created_at', None)
                    lore_data.pop('updated_at', None)
                    lore_data['universe_id'] = target_universe_id
                    
                    lore = Lore(**lore_data)
                    self.session.add(lore)
                    self.session.flush()
                    id_mapping['lore'][old_id] = lore.id
                    stats["total_entities"] += 1
                except Exception as e:
                    stats["errors"].append(f"Lore import error: {str(e)}")
                    stats["skipped"] += 1
        
        # 8. Relationships (last, as they reference other entities)
        if 'relationships' in data:
            for rel_data in data['relationships']:
                try:
                    rel_data.pop('id')
                    rel_data.pop('created_at', None)
                    rel_data.pop('updated_at', None)
                    rel_data['universe_id'] = target_universe_id
                    
                    # Update entity references
                    if rel_data.get('from_entity_id') and rel_data.get('from_entity_type'):
                        entity_type = rel_data['from_entity_type'].lower() + 's'
                        if entity_type in id_mapping and rel_data['from_entity_id'] in id_mapping[entity_type]:
                            rel_data['from_entity_id'] = id_mapping[entity_type][rel_data['from_entity_id']]
                    
                    if rel_data.get('to_entity_id') and rel_data.get('to_entity_type'):
                        entity_type = rel_data['to_entity_type'].lower() + 's'
                        if entity_type in id_mapping and rel_data['to_entity_id'] in id_mapping[entity_type]:
                            rel_data['to_entity_id'] = id_mapping[entity_type][rel_data['to_entity_id']]
                    
                    relationship = Relationship(**rel_data)
                    self.session.add(relationship)
                    self.session.flush()
                    stats["total_entities"] += 1
                except Exception as e:
                    stats["errors"].append(f"Relationship import error: {str(e)}")
                    stats["skipped"] += 1
        
        # Commit all changes
        self.session.commit()
        
        return stats
    
    def _serialize_entity(self, entity: Any) -> Dict[str, Any]:
        """Serialize a SQLAlchemy entity to dictionary.
        
        Args:
            entity: SQLAlchemy model instance
        
        Returns:
            Dictionary representation of entity
        """
        result = {}
        for column in entity.__table__.columns:
            value = getattr(entity, column.name)
            # Convert datetime to ISO format string
            if hasattr(value, 'isoformat'):
                value = value.isoformat()
            # Convert Enum to its value
            elif hasattr(value, 'value'):
                value = value.value
            result[column.name] = value
        return result
