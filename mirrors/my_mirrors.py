from src.event_colors import EventColor
from src.event_rules import Rule, Condition

from src.mirror import Mirror


# Each of theses conditions represent a different course unit

HAI507I_condition = Condition().field('title').contains('HAI507I', case_sensitive=False)  # Calcul formel
HAI501I_condition = Condition().field('title').contains('HAI501I', case_sensitive=False)  # Génie logiciel
HAX503X_HAX505X_condition = Condition().logical_or(Condition().field('title').contains('HAX503X',case_sensitive=False),Condition().field('title').contains('HAX505X',case_sensitive=False))  # Mesure et intégration, Fourier

HAI503I_condition = Condition().field('title').contains('HAI503I', case_sensitive=False)  # Algorithmique 4
HAI504I_condition = Condition().field('title').contains('HAI504I', case_sensitive=False)  # Logique du premier ordre
HAX502X_condition = Condition().field('title').contains('HAX502X', case_sensitive=False)  # Calcul Différentiel et Equations Différentielles
HAX501X_condition = Condition().field('title').contains('HAX501X', case_sensitive=False)  # Groupes et anneaux 1

HAX504X_condition = Condition().field('title').contains('HAX504X', case_sensitive=False)  # Combinatoire énumérative
HAX506X_condition = Condition().field('title').contains('HAX506X', case_sensitive=False) # Théorie des Probabilités


# Each of theses rules change the color of the event, and adds a verbose description of the course unit to the event's title
_supermuel_rules = [
    Rule().prefix_str_to_field('title', 'Calcul formel - ').change_color(EventColor.SAGE).on(HAI507I_condition),

    Rule().prefix_str_to_field('title', 'Génie logiciel - ').change_color(EventColor.PEACOCK).on(HAI501I_condition),

    Rule().prefix_str_to_field('title', 'Mesure et intégration, Fourier - ').change_color(EventColor.TOMATO).on(
        HAX503X_HAX505X_condition),

    Rule().prefix_str_to_field('title', 'Logique du premier ordre - ').change_color(EventColor.GRAPE).on(HAI504I_condition),
    Rule().prefix_str_to_field('title', 'Algorithmique 4 - ').change_color(EventColor.BLUEBERRY).on(HAI503I_condition),

    Rule().prefix_str_to_field('title', 'Calcul Différentiel et Equations Différentielles - ').change_color(EventColor.TANGERINE).on(HAX502X_condition),

    Rule().prefix_str_to_field('title', 'Groupes et anneaux 1 - ').on(HAX501X_condition),

    Rule().remove_event().on(HAX504X_condition),

    Rule().prefix_str_to_field('title', 'Théorie des Probabilités - ').change_color(
        EventColor.BANANA).on(HAX506X_condition),

]


my_mirror = Mirror(title="L3_maths_info",
                 source_ics_calendar_url="https://proseconsult.umontpellier.fr/jsp/custom/modules/plannings/direct_cal.jsp?data=...,1",
                 google_calendar_id="<YOUR_GOOGLE_CALENDAR_ID",
                 rules=_supermuel_rules)

