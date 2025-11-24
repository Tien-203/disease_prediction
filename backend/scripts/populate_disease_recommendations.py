"""Migration script to populate disease recommendations in database"""
import sys
from pathlib import Path

# Add backend directory to Python path when run as script
if __name__ == "__main__":
    backend_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from loguru import logger
from app.db.session import SessionLocal
from app.models.disease import Disease

# Comprehensive recommendations for each disease
DISEASE_RECOMMENDATIONS = {
    "(vertigo) Paroymsal  Positional Vertigo": [
        "Avoid sudden head movements",
        "Move slowly when changing positions",
        "Sleep with head elevated",
        "Perform vestibular rehabilitation exercises",
        "Consult with an ENT specialist for proper diagnosis"
    ],
    "AIDS": [
        "Take antiretroviral therapy (ART) as prescribed",
        "Practice safe sex and use protection",
        "Get regular medical checkups",
        "Maintain a healthy diet and lifestyle",
        "Avoid sharing needles or personal items",
        "Seek support from healthcare providers and support groups"
    ],
    "Acne": [
        "Wash face twice daily with gentle cleanser",
        "Avoid picking or squeezing pimples",
        "Use non-comedogenic skincare products",
        "Keep skin moisturized",
        "Consider over-the-counter treatments with benzoyl peroxide or salicylic acid",
        "Consult dermatologist if condition persists"
    ],
    "Alcoholic hepatitis": [
        "Immediately stop alcohol consumption",
        "Follow a balanced, nutritious diet",
        "Take prescribed medications as directed",
        "Get regular liver function tests",
        "Consider joining alcohol support programs",
        "Rest and avoid strenuous activities"
    ],
    "Allergy": [
        "Identify and avoid allergens",
        "Take antihistamines as prescribed",
        "Keep environment clean and dust-free",
        "Use air purifiers if needed",
        "Carry epinephrine auto-injector if severe",
        "Consult allergist for allergy testing"
    ],
    "Arthritis": [
        "Maintain regular exercise with low-impact activities",
        "Apply heat or cold therapy to affected joints",
        "Take anti-inflammatory medications as prescribed",
        "Maintain healthy weight",
        "Use assistive devices if needed",
        "Consider physical therapy"
    ],
    "Bronchial Asthma": [
        "Avoid triggers (dust, pollen, smoke)",
        "Use inhalers as prescribed",
        "Keep rescue inhaler with you at all times",
        "Monitor peak flow regularly",
        "Create an asthma action plan with your doctor",
        "Get flu and pneumonia vaccinations"
    ],
    "Cervical spondylosis": [
        "Maintain good posture",
        "Perform neck exercises regularly",
        "Use ergonomic workstation setup",
        "Apply heat or cold therapy",
        "Take pain medications as prescribed",
        "Consider physical therapy"
    ],
    "Chicken pox": [
        "Stay home and rest until blisters scab over",
        "Keep skin clean and dry",
        "Apply calamine lotion to reduce itching",
        "Take acetaminophen for fever (avoid aspirin)",
        "Drink plenty of fluids",
        "Avoid scratching to prevent scarring"
    ],
    "Chronic cholestasis": [
        "Follow liver-friendly diet (low fat, high protein)",
        "Take prescribed medications regularly",
        "Avoid alcohol completely",
        "Get regular liver function monitoring",
        "Manage itching with prescribed medications",
        "Consult hepatologist for specialized care"
    ],
    "Common Cold": [
        "Get plenty of rest",
        "Drink lots of fluids (water, tea, soup)",
        "Use saline nasal sprays",
        "Gargle with warm salt water",
        "Take over-the-counter cold medications",
        "Wash hands frequently to prevent spread"
    ],
    "Dengue": [
        "Get plenty of rest",
        "Stay well hydrated",
        "Take acetaminophen for fever (avoid aspirin/NSAIDs)",
        "Monitor for warning signs (severe pain, bleeding)",
        "Seek immediate medical attention if symptoms worsen",
        "Use mosquito repellent to prevent further bites"
    ],
    "Diabetes ": [
        "Monitor blood sugar levels regularly",
        "Follow diabetic diet plan",
        "Take medications or insulin as prescribed",
        "Exercise regularly",
        "Get regular eye and foot exams",
        "Maintain healthy weight"
    ],
    "Dimorphic hemmorhoids(piles)": [
        "Increase fiber intake in diet",
        "Drink plenty of water",
        "Avoid straining during bowel movements",
        "Use sitz baths for relief",
        "Apply topical treatments as prescribed",
        "Consider stool softeners if needed"
    ],
    "Drug Reaction": [
        "Stop taking the medication immediately",
        "Seek medical attention if severe",
        "Take antihistamines if prescribed",
        "Apply cool compresses to affected areas",
        "Keep a record of the reaction",
        "Inform all healthcare providers about drug allergies"
    ],
    "Fungal infection": [
        "Keep affected area clean and dry",
        "Apply antifungal creams as directed",
        "Wear breathable clothing",
        "Avoid sharing personal items",
        "Change clothes and towels regularly",
        "Complete full course of treatment"
    ],
    "GERD": [
        "Eat smaller, more frequent meals",
        "Avoid trigger foods (spicy, fatty, acidic)",
        "Don't lie down immediately after eating",
        "Elevate head of bed",
        "Take antacids or prescribed medications",
        "Maintain healthy weight"
    ],
    "Gastroenteritis": [
        "Stay hydrated with oral rehydration solutions",
        "Eat bland foods (BRAT diet: bananas, rice, applesauce, toast)",
        "Avoid dairy and fatty foods",
        "Get plenty of rest",
        "Wash hands frequently",
        "Seek medical attention if severe dehydration occurs"
    ],
    "Heart attack": [
        "Call emergency services immediately (911)",
        "Chew and swallow aspirin if not allergic",
        "Stay calm and rest",
        "Do not drive yourself to hospital",
        "Follow emergency medical instructions",
        "After treatment, follow cardiac rehabilitation program"
    ],
    "Hepatitis B": [
        "Get vaccinated if not already",
        "Take antiviral medications as prescribed",
        "Avoid alcohol completely",
        "Follow liver-friendly diet",
        "Get regular liver function tests",
        "Inform close contacts to get tested"
    ],
    "Hepatitis C": [
        "Take antiviral medications as prescribed",
        "Avoid alcohol completely",
        "Follow liver-friendly diet",
        "Get regular liver function monitoring",
        "Consider hepatitis A and B vaccinations",
        "Inform close contacts to get tested"
    ],
    "Hepatitis D": [
        "Take prescribed medications",
        "Avoid alcohol completely",
        "Follow liver-friendly diet",
        "Get regular liver function tests",
        "Prevent hepatitis B (HDV requires HBV)",
        "Consult hepatologist for specialized care"
    ],
    "Hepatitis E": [
        "Get plenty of rest",
        "Stay well hydrated",
        "Avoid alcohol",
        "Follow liver-friendly diet",
        "Practice good hygiene",
        "Get regular liver function monitoring"
    ],
    "Hypertension ": [
        "Monitor blood pressure regularly",
        "Take medications as prescribed",
        "Reduce sodium intake",
        "Exercise regularly",
        "Maintain healthy weight",
        "Limit alcohol and quit smoking"
    ],
    "Hyperthyroidism": [
        "Take antithyroid medications as prescribed",
        "Avoid iodine-rich foods if advised",
        "Monitor thyroid function regularly",
        "Manage stress levels",
        "Get adequate rest",
        "Follow up with endocrinologist"
    ],
    "Hypoglycemia": [
        "Eat regular, balanced meals",
        "Carry glucose tablets or snacks",
        "Monitor blood sugar levels",
        "Eat complex carbohydrates",
        "Avoid skipping meals",
        "Wear medical alert bracelet"
    ],
    "Hypothyroidism": [
        "Take thyroid hormone replacement as prescribed",
        "Take medication on empty stomach",
        "Get regular thyroid function tests",
        "Follow up with endocrinologist",
        "Maintain healthy diet",
        "Be patient with treatment (takes time to work)"
    ],
    "Impetigo": [
        "Keep affected areas clean",
        "Apply prescribed antibiotic ointments",
        "Wash hands frequently",
        "Avoid touching or scratching lesions",
        "Use separate towels and washcloths",
        "Complete full course of antibiotics"
    ],
    "Jaundice": [
        "Identify and treat underlying cause",
        "Stay well hydrated",
        "Follow liver-friendly diet",
        "Avoid alcohol",
        "Get regular liver function tests",
        "Rest and avoid strenuous activities"
    ],
    "Malaria": [
        "Take antimalarial medications as prescribed",
        "Complete full course of treatment",
        "Stay well hydrated",
        "Get plenty of rest",
        "Use mosquito nets and repellents",
        "Seek immediate medical attention if severe"
    ],
    "Migraine": [
        "Rest in a dark, quiet room",
        "Apply cold compress to forehead",
        "Take prescribed migraine medications",
        "Identify and avoid triggers",
        "Stay hydrated",
        "Consider preventive medications if frequent"
    ],
    "Osteoarthristis": [
        "Maintain regular low-impact exercise",
        "Apply heat or cold therapy",
        "Take pain medications as prescribed",
        "Maintain healthy weight",
        "Use assistive devices if needed",
        "Consider physical therapy"
    ],
    "Paralysis (brain hemorrhage)": [
        "Seek immediate emergency medical care",
        "Follow rehabilitation program",
        "Work with physical and occupational therapists",
        "Take medications as prescribed",
        "Monitor for complications",
        "Get support from family and caregivers"
    ],
    "Peptic ulcer diseae": [
        "Take prescribed medications (PPIs, antibiotics if H. pylori)",
        "Avoid NSAIDs and aspirin",
        "Eat smaller, more frequent meals",
        "Avoid spicy and acidic foods",
        "Reduce stress",
        "Avoid smoking and limit alcohol"
    ],
    "Pneumonia": [
        "Get plenty of rest",
        "Stay well hydrated",
        "Take antibiotics as prescribed (complete full course)",
        "Use humidifier to ease breathing",
        "Take fever reducers if needed",
        "Seek immediate care if breathing difficulties worsen"
    ],
    "Psoriasis": [
        "Keep skin moisturized",
        "Use prescribed topical treatments",
        "Avoid triggers (stress, infections, injuries)",
        "Get regular sunlight exposure (with doctor's approval)",
        "Consider phototherapy if recommended",
        "Manage stress levels"
    ],
    "Tuberculosis": [
        "Take all prescribed medications (complete full course)",
        "Take medications exactly as directed",
        "Isolate until no longer contagious (as advised by doctor)",
        "Get regular follow-up appointments",
        "Inform close contacts to get tested",
        "Maintain good nutrition"
    ],
    "Typhoid": [
        "Take antibiotics as prescribed (complete full course)",
        "Stay well hydrated",
        "Get plenty of rest",
        "Eat soft, easily digestible foods",
        "Practice good hygiene",
        "Seek immediate care if severe symptoms"
    ],
    "Urinary tract infection": [
        "Drink plenty of water",
        "Take antibiotics as prescribed (complete full course)",
        "Urinate frequently",
        "Avoid holding urine",
        "Wipe from front to back",
        "Avoid irritating products"
    ],
    "Varicose veins": [
        "Elevate legs when resting",
        "Wear compression stockings",
        "Exercise regularly (walking, swimming)",
        "Avoid standing or sitting for long periods",
        "Maintain healthy weight",
        "Consider medical procedures if severe"
    ],
    "hepatitis A": [
        "Get plenty of rest",
        "Stay well hydrated",
        "Avoid alcohol",
        "Follow liver-friendly diet",
        "Practice good hygiene",
        "Get hepatitis A vaccination if not already"
    ]
}


def populate_recommendations():
    """Populate recommendations for all diseases in database"""
    db = SessionLocal()
    try:
        logger.info("Starting to populate disease recommendations...")
        
        updated_count = 0
        created_count = 0
        
        for disease_name, recommendations in DISEASE_RECOMMENDATIONS.items():
            # Find disease by name (case-insensitive)
            disease = db.query(Disease).filter(
                Disease.name.ilike(disease_name.strip())
            ).first()
            
            if disease:
                # Convert list to string (newline-separated)
                recommendations_str = "\n".join(recommendations)
                
                if disease.recommendations != recommendations_str:
                    disease.recommendations = recommendations_str
                    updated_count += 1
                    logger.info(f"Updated recommendations for: {disease.name}")
                else:
                    logger.debug(f"Recommendations already up to date for: {disease.name}")
            else:
                # Disease not found, log warning
                logger.warning(f"Disease not found in database: {disease_name}")
                created_count += 1
        
        db.commit()
        
        logger.success(f"Successfully populated recommendations!")
        logger.info(f"  - Updated: {updated_count} diseases")
        logger.info(f"  - Not found: {created_count} diseases")
        
        return True
    except Exception as e:
        logger.error(f"Error populating recommendations: {e}")
        db.rollback()
        import traceback
        logger.error(traceback.format_exc())
        return False
    finally:
        db.close()


if __name__ == "__main__":
    success = populate_recommendations()
    sys.exit(0 if success else 1)




