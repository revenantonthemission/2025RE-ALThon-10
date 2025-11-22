"""
Vector Seeding Script for User Embeddings

This script generates and updates embedding vectors for all users in the database
based on their profile information (interests, preferences, course history).
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from loguru import logger
import sys
import os

# Add backend to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db.database import SessionLocal
from backend.models.user import User, UserCourse
from backend.core.encoder import generate_embeddings


def create_user_profile_text(user: User, courses: List[UserCourse]) -> str:
    """
    Create a text representation of a user's profile for embedding generation.
    
    Args:
        user: User model instance
        courses: List of UserCourse instances for this user
        
    Returns:
        Formatted text string representing the user's profile
    """
    # Build course history summary
    course_summary = []
    for course in courses:
        grade_desc = f"{course.course_name} ({course.course_code}): {course.grade_point:.1f}"
        course_summary.append(grade_desc)
    
    courses_text = ", ".join(course_summary) if course_summary else "없음"
    
    # Create comprehensive profile text
    profile_text = f"""
    학생 정보:
    - 학번: {user.student_id}
    - 전공: {user.major}
    - 학년: {user.grade_level}학년
    - 수강 이력: {courses_text}
    """.strip()
    
    return profile_text


def seed_user_vectors(batch_size: int = 10, user_limit: int = None):
    """
    Generate and update embedding vectors for all users in the database.
    
    Args:
        batch_size: Number of users to process in each batch
        user_limit: Maximum number of users to process (None = all users)
    """
    logger.info("Starting user vector seeding process...")
    
    db: Session = SessionLocal()
    
    try:
        # Get all users (or limited number)
        query = select(User)
        if user_limit:
            query = query.limit(user_limit)
        
        users = db.execute(query).scalars().all()
        total_users = len(users)
        
        if total_users == 0:
            logger.warning("No users found in database. Nothing to seed.")
            return
        
        logger.info(f"Found {total_users} users to process")
        
        # Process users in batches
        updated_count = 0
        failed_count = 0
        
        for i in range(0, total_users, batch_size):
            batch = users[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total_users + batch_size - 1) // batch_size
            
            logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} users)")
            
            # Prepare profile texts for this batch
            profile_texts = []
            user_course_map = {}
            
            for user in batch:
                # Get user's courses
                courses = db.query(UserCourse).filter(UserCourse.user_id == user.id).all()
                user_course_map[user.id] = courses
                
                # Create profile text
                profile_text = create_user_profile_text(user, courses)
                profile_texts.append(profile_text)
            
            try:
                # Generate embeddings for the batch
                logger.debug(f"Generating embeddings for batch {batch_num}...")
                embeddings = generate_embeddings(profile_texts, batch_size=len(profile_texts))
                
                if len(embeddings) != len(batch):
                    logger.error(f"Embedding count mismatch: expected {len(batch)}, got {len(embeddings)}")
                    failed_count += len(batch)
                    continue
                
                # Update each user with their embedding
                for user, embedding in zip(batch, embeddings):
                    user.embedding = embedding
                    updated_count += 1
                
                # Commit the batch
                db.commit()
                logger.success(f"Batch {batch_num} completed: {len(batch)} users updated")
                
            except Exception as e:
                logger.error(f"Failed to process batch {batch_num}: {e}")
                db.rollback()
                failed_count += len(batch)
        
        # Final summary
        logger.info("=" * 60)
        logger.success(f"Vector seeding completed!")
        logger.info(f"Total users processed: {total_users}")
        logger.info(f"Successfully updated: {updated_count}")
        logger.info(f"Failed: {failed_count}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Fatal error during vector seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Seed user embedding vectors")
    parser.add_argument("--batch-size", type=int, default=10, help="Batch size for processing (default: 10)")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of users to process (default: all)")
    
    args = parser.parse_args()
    
    seed_user_vectors(batch_size=args.batch_size, user_limit=args.limit)
