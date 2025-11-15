"""
Stage Manager - Model stage transition logic

Handles stage-based deployment workflow (Dev → Staging → Production).
"""

from typing import Optional, Dict, List
import logging

from config.settings import (
    STAGE_DEV,
    STAGE_STAGING,
    STAGE_PRODUCTION,
    STAGE_ARCHIVED,
)
from registry.core.model_manager import ModelManager
from registry.utils.logging_utils import setup_logger

logger = setup_logger(__name__)


class StageManager:
    """Manages model stage transitions and lifecycle."""
    
    # Define allowed transitions (None = Development/Unassigned)
    ALLOWED_TRANSITIONS = {
        STAGE_DEV: [STAGE_STAGING, STAGE_ARCHIVED],  # None -> Staging or Archived
        STAGE_STAGING: [STAGE_PRODUCTION, STAGE_DEV, STAGE_ARCHIVED],
        STAGE_PRODUCTION: [STAGE_ARCHIVED, STAGE_STAGING],  # Allow rollback to Staging
        STAGE_ARCHIVED: [STAGE_DEV, STAGE_STAGING],  # Allow re-activation
    }
    
    def __init__(self):
        """Initialize StageManager."""
        self.model_manager = ModelManager()
        logger.info("StageManager initialized")
    
    def promote_to_staging(
        self,
        model_name: str,
        version: str,
        archive_existing: bool = True,
    ) -> None:
        """
        Promote a model from Development to Staging.
        
        Args:
            model_name: Name of the registered model
            version: Version to promote
            archive_existing: Whether to archive existing staging versions
        """
        self._validate_and_transition(
            model_name=model_name,
            version=version,
            target_stage=STAGE_STAGING,
            expected_current_stage=STAGE_DEV,
            archive_existing=archive_existing,
        )
        logger.info(f"Promoted {model_name} v{version} to Staging")
    
    def promote_to_production(
        self,
        model_name: str,
        version: str,
        archive_existing: bool = True,
    ) -> None:
        """
        Promote a model from Staging to Production.
        
        Args:
            model_name: Name of the registered model
            version: Version to promote
            archive_existing: Whether to archive existing production versions
        """
        self._validate_and_transition(
            model_name=model_name,
            version=version,
            target_stage=STAGE_PRODUCTION,
            expected_current_stage=STAGE_STAGING,
            archive_existing=archive_existing,
        )
        logger.info(f"Promoted {model_name} v{version} to Production")
    
    def demote_to_development(
        self,
        model_name: str,
        version: str,
    ) -> None:
        """
        Demote a model back to Development.
        
        Args:
            model_name: Name of the registered model
            version: Version to demote
        """
        self.model_manager.transition_stage(
            model_name=model_name,
            version=version,
            stage=STAGE_DEV,
            archive_existing=False,
        )
        logger.info(f"Demoted {model_name} v{version} to Development")
    
    def archive_model(
        self,
        model_name: str,
        version: str,
    ) -> None:
        """
        Archive a model version.
        
        Args:
            model_name: Name of the registered model
            version: Version to archive
        """
        self.model_manager.transition_stage(
            model_name=model_name,
            version=version,
            stage=STAGE_ARCHIVED,
            archive_existing=False,
        )
        logger.info(f"Archived {model_name} v{version}")
    
    def _validate_and_transition(
        self,
        model_name: str,
        version: str,
        target_stage: str,
        expected_current_stage: Optional[str] = None,
        archive_existing: bool = True,
    ) -> None:
        """
        Validate and perform stage transition.
        
        Args:
            model_name: Name of the registered model
            version: Version to transition
            target_stage: Target stage
            expected_current_stage: Expected current stage (or None to skip check)
            archive_existing: Whether to archive existing versions
        """
        # Get current version
        model_version = self.model_manager.get_model_version(
            model_name=model_name,
            version=version,
        )
        
        current_stage = model_version.current_stage
        
        # Validate current stage if specified
        if expected_current_stage and current_stage != expected_current_stage:
            raise ValueError(
                f"Model is in '{current_stage}' stage, "
                f"expected '{expected_current_stage}'"
            )
        
        # Validate transition is allowed
        if current_stage in self.ALLOWED_TRANSITIONS:
            allowed_targets = self.ALLOWED_TRANSITIONS[current_stage]
            if target_stage not in allowed_targets:
                raise ValueError(
                    f"Transition from '{current_stage}' to '{target_stage}' "
                    f"is not allowed. Allowed targets: {allowed_targets}"
                )
        
        # Perform transition
        self.model_manager.transition_stage(
            model_name=model_name,
            version=version,
            stage=target_stage,
            archive_existing=archive_existing,
        )
    
    def get_stage_info(self, model_name: str) -> Dict[str, List[str]]:
        """
        Get information about model versions in each stage.
        
        Args:
            model_name: Name of the registered model
            
        Returns:
            Dictionary mapping stages to version lists
        """
        versions = self.model_manager.list_model_versions(model_name)
        
        stage_info = {
            STAGE_DEV: [],
            STAGE_STAGING: [],
            STAGE_PRODUCTION: [],
            STAGE_ARCHIVED: [],
        }
        
        for version in versions:
            stage = version.current_stage
            if stage in stage_info:
                stage_info[stage].append(version.version)
        
        return stage_info
    
    def get_production_model(self, model_name: str) -> Optional[str]:
        """
        Get the current production model version.
        
        Args:
            model_name: Name of the registered model
            
        Returns:
            Production version number or None
        """
        try:
            model_version = self.model_manager.get_model_version(
                model_name=model_name,
                stage=STAGE_PRODUCTION,
            )
            return model_version.version
            
        except ValueError:
            return None
    
    def rollback_production(
        self,
        model_name: str,
        target_version: str,
    ) -> None:
        """
        Rollback production to a specific version.
        
        Args:
            model_name: Name of the registered model
            target_version: Version to rollback to
        """
        # Get target version
        target = self.model_manager.get_model_version(
            model_name=model_name,
            version=target_version,
        )
        
        # Must be in Archived or Staging
        if target.current_stage not in [STAGE_ARCHIVED, STAGE_STAGING]:
            raise ValueError(
                f"Can only rollback to Archived or Staging versions. "
                f"Version {target_version} is in '{target.current_stage}'"
            )
        
        # Promote to production
        self.model_manager.transition_stage(
            model_name=model_name,
            version=target_version,
            stage=STAGE_PRODUCTION,
            archive_existing=True,
        )
        
        logger.info(f"Rolled back {model_name} production to v{target_version}")