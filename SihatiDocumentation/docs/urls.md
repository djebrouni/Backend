# Fichier des URLs du Projet DPI Gestion

## 1. Routes Principales

### **Application Utilisateurs (`users`)**
- `/` : Inclus les URLs de l'application utilisateurs.

### **Application Authentification (`auth`)**
- `/auth/` : Inclus les URLs de l'application authentification.

### **Application Médecins (`medecins`)**
- `/medecins/` : Inclus les URLs de l'application médecins.

### **Application Patients (`patients`)**
- `/patients/` : Inclus les URLs de l'application patients.

### **Application Infirmiers (`infermier`)**
- `/infermier/` : Inclus les URLs de l'application infirmiers.

### **Application Techniciens de Laboratoire (`labtechnicians`)**
- `/labtechnicians/` : Inclus les URLs de l'application techniciens de laboratoire.

### **Application Recherche (`get`)**
- `/get/` : Inclus les URLs de l'application recherche.

### **Application Système de Gestion de Prescription (`sgph`)**
- `/sgph/` : Inclus les URLs de l'application SGPH.

## 2. Validation de Prescription et Liste des Prescriptions

### **Validation des prescriptions**
- `/validate-prescription/` : `POST` pour valider une prescription.

### **Liste des prescriptions**
- `/list-prescriptions/` : `GET` pour afficher la liste des prescriptions.

## 3. Gestion des Patients

### **Créer un patient DPI**
- `/create_patient_dpi/` : `POST` pour créer un patient DPI.

### **Consulter un patient DPI**
- `/consultation-dpi/` : `GET` pour consulter les données DPI d'un patient.

### **Mettre à jour le profil utilisateur**
- `/update-profile/` : `PUT` pour mettre à jour le profil de l'utilisateur.

### **Afficher le profil utilisateur**
- `/profile/` : `GET` pour afficher les informations du profil de l'utilisateur.

## 4. Consultation Médicale

### **Créer une consultation**
- `/consultation/create/` : `POST` pour créer une consultation.

### **Mettre à jour une consultation**
- `/consultation/update/<int:consultation_id>/` : `PUT` pour mettre à jour une consultation existante.

### **Afficher le résumé d'une consultation**
- `/consultation/summary/<int:consultation_id>/` : `GET` pour afficher le résumé d'une consultation.

## 5. Bilan Biologique et Radiologique

### **Créer un bilan biologique**
- `/create_biological_assessment/<int:ehr_id>/` : `POST` pour créer un bilan biologique.

### **Afficher un bilan biologique**
- `/view_biological_assessment/<int:ehr_id>/` : `GET` pour afficher les résultats d'un bilan biologique.

### **Remplir un rapport biologique**
- `/biological_assessment/fill_report/<int:assessment_id>/` : `POST` pour remplir un rapport biologique.

### **Afficher un rapport biologique**
- `/biological_assessment/display_report/<int:assessment_id>/` : `GET` pour afficher un rapport biologique.

### **Créer un bilan radiologique**
- `/create_radiology_assessment/<int:ehr_id>/` : `POST` pour créer un bilan radiologique.

### **Afficher un bilan radiologique**
- `/display_radiology_assessment/<int:ehr_id>/` : `GET` pour afficher les résultats d'un bilan radiologique.

### **Remplir un rapport radiologique**
- `/fill-radiology-report/<int:assessment_id>/` : `POST` pour remplir un rapport radiologique.

### **Afficher un rapport radiologique**
- `/display-radiology-report/<int:assessment_id>/` : `GET` pour afficher un rapport radiologique.

## 6. Recherche et Affichage des Rapports

### **Afficher les rapports biologiques**
- `/biology-reports/` : `GET` pour consulter tous les rapports biologiques.

### **Afficher les rapports radiologiques**
- `/radiology-reports/` : `GET` pour consulter tous les rapports radiologiques.

### **Rechercher un patient par NSS**
- `/search-patient/` : `GET` pour rechercher un patient par son numéro de sécurité sociale.

## 7. Création de Prescriptions

### **Créer une prescription**
- `/prescriptions/create/` : `POST` pour créer une prescription.

## 8. Gestion des Soins

### **Créer un soin fourni**
- `/careprovided/create/` : `POST` pour créer un soin fourni.

### **Afficher un soin fourni**
- `/careprovided/<int:care_provided_id>/` : `GET` pour afficher les détails d'un soin fourni.

### **Mettre à jour un soin fourni**
- `/careprovided/update/<int:care_provided_id>/` : `PUT` pour mettre à jour un soin fourni.

## 9. Enregistrements Médicaux

### **Afficher les dossiers hospitaliers**
- `/hospital-records/` : `GET` pour afficher les dossiers hospitaliers.

### **Afficher les dossiers des médecins**
- `/doctor-records/` : `GET` pour afficher les dossiers des médecins.

### **Afficher les détails d'une prescription**
- `/prescription/<int:prescription_id>/` : `GET` pour afficher les détails d'une prescription.

### **Afficher les détails d'un soin fourni**
- `/careprovided/<int:care_id>/` : `GET` pour afficher les détails d'un soin fourni.

## 10. Authentification et Inscription

### **Se connecter**
- `/signin` : `POST` pour la connexion d'un utilisateur.

### **S'inscrire**
- `/signup` : `POST` pour l'inscription d'un nouvel utilisateur.

## 11. Tendances Médicales

### **Générer les tendances de la glycémie**
- `/generate_blood_sugar_trend/` : `GET` pour générer les tendances de la glycémie.

### **Générer les tendances de la pression artérielle**
- `/generate_blood_pressure_trend/` : `GET` pour générer les tendances de la pression artérielle.

### **Générer les tendances du cholestérol**
- `/generate_cholesterol_level_trend/` : `GET` pour générer les tendances du cholestérol.

### **Générer les tendances de la numération sanguine complète**
- `/generate_complete_blood_count_trend/` : `GET` pour générer les tendances de la numération sanguine complète.
