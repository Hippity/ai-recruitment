from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)

    # one-to-one
    personal_information = db.relationship(
        'PersonalInformation', backref='application',
        uselist=False, lazy=True
    )
    other_information = db.relationship(
        'OtherInformation', backref='application',
        uselist=False, lazy=True
    )

    # one-to-many
    addresses = db.relationship('Address', lazy=True, backref='application')
    universities = db.relationship('University', lazy=True, backref='application')
    trainings = db.relationship('Training', lazy=True, backref='application')
    secondary_schools = db.relationship('SecondarySchool', lazy=True, backref='application')
    professional_experiences = db.relationship(
        'ProfessionalExperience', lazy=True, backref='application'
    )
    languages = db.relationship('Language', lazy=True, backref='application')


class PersonalInformation(db.Model):
    __tablename__ = 'personal_information'

    id                                       = db.Column(db.Integer, primary_key=True)
    application_id                           = db.Column(
        db.Integer, db.ForeignKey('applications.id', ondelete='CASCADE'),
        nullable=False
    )

    # core personal data
    first_name                               = db.Column(db.String(100), nullable=False)
    middle_name                              = db.Column(db.String(100), nullable=False)
    last_name                                = db.Column(db.String(100), nullable=False)
    mothers_name                             = db.Column(db.String(255), nullable=False)
    sex                                      = db.Column(
        db.Enum('Male', 'Female', name='sex_enum'), nullable=False
    )
    marital_status                           = db.Column(
        db.Enum('Single', 'Divorced', 'Married', 'Widow', name='marital_status_enum'),
        nullable=False
    )
    holds_lebanese_citizenship_more_than_ten_years = db.Column(
        db.Boolean, nullable=False, default=False
    )
    place_of_registration                    = db.Column(db.String(255), nullable=False)
    sect                                     = db.Column(db.String(100), nullable=False)
    date_of_birth                            = db.Column(db.Date, nullable=False)
    national_id_no                           = db.Column(db.String(50), nullable=False)
    lebanese_passport_no                     = db.Column(db.String(50), nullable=True)
    governorate                              = db.Column(db.String(100), nullable=False)
    caza                                     = db.Column(db.String(100), nullable=False)

    # ─── Years of Experience ─────────────────────────────────────────────────────
    years_in_public_sector                   = db.Column(db.Float, nullable=False, default=0.0)
    years_in_private_sector                  = db.Column(db.Float, nullable=False, default=0.0)
    total_years_of_experience                = db.Column(db.Float, nullable=False, default=0.0)

    # ─── Computer proficiency ────────────────────────────────────────────────────
    computer_tools_proficiency               = db.Column(db.Boolean, nullable=False, default=False)
    computer_tools_proficiency_level         = db.Column(
        db.Enum('Excellent', 'Good', 'Fair', name='computer_tools_proficiency_level_enum'),
        nullable=True
    )

    # ─── Public‐sector history ───────────────────────────────────────────────────
    worked_previously_in_public_sector       = db.Column(db.Boolean, nullable=False, default=False)
    member_of_cadre                          = db.Column(db.Boolean, nullable=False, default=False)
    public_admin_job_type                    = db.Column(db.String(100), nullable=True)
    grade_i_public_servant                   = db.Column(db.Boolean, nullable=False, default=False)
    grade_ii_public_servant                  = db.Column(db.Boolean, nullable=False, default=False)
    grade_ii_degree                          = db.Column(db.String(50), nullable=True)
    grade_iii_public_servant                 = db.Column(db.Boolean, nullable=False, default=False)
    grade_iii_degree                         = db.Column(db.String(50), nullable=True)
    public_servant_position_description      = db.Column(db.Text, nullable=True)

    # ─── Additional Skills ──────────────────────────────────────────────────────
    additional_skills                        = db.Column(db.Text, nullable=True)

    created_at                               = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'mothers_name': self.mothers_name,
            'sex': self.sex,
            'marital_status': self.marital_status,
            'holds_lebanese_citizenship_more_than_ten_years': self.holds_lebanese_citizenship_more_than_ten_years,
            'place_of_registration': self.place_of_registration,
            'sect': self.sect,
            'date_of_birth': self.date_of_birth.isoformat(),
            'national_id_no': self.national_id_no,
            'lebanese_passport_no': self.lebanese_passport_no,
            'governorate': self.governorate,
            'caza': self.caza,
            'years_in_public_sector': self.years_in_public_sector,
            'years_in_private_sector': self.years_in_private_sector,
            'total_years_of_experience': self.total_years_of_experience,
            'computer_tools_proficiency': self.computer_tools_proficiency,
            'computer_tools_proficiency_level': self.computer_tools_proficiency_level,
            'worked_previously_in_public_sector': self.worked_previously_in_public_sector,
            'member_of_cadre': self.member_of_cadre,
            'public_admin_job_type': self.public_admin_job_type,
            'grade_i_public_servant': self.grade_i_public_servant,
            'grade_ii_public_servant': self.grade_ii_public_servant,
            'grade_ii_degree': self.grade_ii_degree,
            'grade_iii_public_servant': self.grade_iii_public_servant,
            'grade_iii_degree': self.grade_iii_degree,
            'public_servant_position_description': self.public_servant_position_description,
            'additional_skills': self.additional_skills,
            'created_at': self.created_at.isoformat()
        }


class Address(db.Model):
    __tablename__ = 'addresses'
    id              = db.Column(db.Integer, primary_key=True)
    application_id  = db.Column(
        db.Integer, db.ForeignKey('applications.id', ondelete='CASCADE'),
        nullable=False
    )
    address_type    = db.Column(
        db.Enum('Permanent', 'Current', name='address_type_enum'),
        nullable=False
    )
    country         = db.Column(db.String(100), nullable=False)
    address_line    = db.Column(db.Text, nullable=False)
    phone_no        = db.Column(db.String(50), nullable=True)
    mobile          = db.Column(db.String(50), nullable=False)
    fax             = db.Column(db.String(50), nullable=True)
    email           = db.Column(db.String(255), nullable=True)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'address_type': self.address_type,
            'country': self.country,
            'address_line': self.address_line,
            'phone_no': self.phone_no,
            'mobile': self.mobile,
            'fax': self.fax,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


class University(db.Model):
    __tablename__ = 'universities'
    id                   = db.Column(db.Integer, primary_key=True)
    application_id       = db.Column(
        db.Integer, db.ForeignKey('applications.id', ondelete='CASCADE'),
        nullable=False
    )
    university_name      = db.Column(db.String(255), nullable=False)
    country              = db.Column(db.String(100), nullable=False)
    address_line         = db.Column(db.Text, nullable=False)
    degree               = db.Column(db.String(100), nullable=False)
    academic_distinction = db.Column(db.String(100), nullable=True)
    specialization       = db.Column(db.String(100), nullable=False)
    start_date           = db.Column(db.Date, nullable=False)
    end_date             = db.Column(db.Date, nullable=True)
    created_at           = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'university_name': self.university_name,
            'country': self.country,
            'address_line': self.address_line,
            'degree': self.degree,
            'academic_distinction': self.academic_distinction,
            'specialization': self.specialization,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat()
        }


class Training(db.Model):
    __tablename__ = 'trainings'
    id                   = db.Column(db.Integer, primary_key=True)
    application_id       = db.Column(
        db.Integer, db.ForeignKey('applications.id', ondelete='CASCADE'),
        nullable=False
    )
    institution_name     = db.Column(db.String(255), nullable=False)
    institution_type     = db.Column(db.String(100), nullable=False)
    country              = db.Column(db.String(100), nullable=False)
    address_line         = db.Column(db.Text, nullable=False)
    degrees              = db.Column(db.String(255), nullable=False)
    major                = db.Column(db.String(100), nullable=True)
    start_date           = db.Column(db.Date, nullable=False)
    end_date             = db.Column(db.Date, nullable=True)
    created_at           = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'institution_name': self.institution_name,
            'institution_type': self.institution_type,
            'country': self.country,
            'address_line': self.address_line,
            'degrees': self.degrees,
            'major': self.major,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat()
        }


class SecondarySchool(db.Model):
    __tablename__ = 'secondary_schools'
    id                       = db.Column(db.Integer, primary_key=True)
    application_id           = db.Column(
        db.Integer, db.ForeignKey('applications.id', ondelete='CASCADE'),
        nullable=False
    )
    school_name              = db.Column(db.String(255), nullable=False)
    country                  = db.Column(db.String(100), nullable=False)
    address_line             = db.Column(db.Text, nullable=False)
    certificates_obtained    = db.Column(db.String(255), nullable=False)
    start_date               = db.Column(db.Date, nullable=False)
    end_date                 = db.Column(db.Date, nullable=True)
    created_at               = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'school_name': self.school_name,
            'country': self.country,
            'address_line': self.address_line,
            'certificates_obtained': self.certificates_obtained,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat()
        }


class ProfessionalExperience(db.Model):
    __tablename__ = 'professional_experiences'
    id                                = db.Column(db.Integer, primary_key=True)
    application_id                    = db.Column(
        db.Integer, db.ForeignKey('applications.id', ondelete='CASCADE'),
        nullable=False
    )
    type_of_business                  = db.Column(
        db.Enum('Public Sector', 'Private Sector', name='business_type_enum'),
        nullable=False
    )
    name_of_employer                  = db.Column(db.String(255), nullable=False)
    type_of_work                      = db.Column(db.String(255), nullable=True)
    address_line                      = db.Column(db.Text, nullable=False)
    phone                             = db.Column(db.String(50), nullable=True)
    fax                               = db.Column(db.String(50), nullable=True)
    current_or_previous_position      = db.Column(db.String(100), nullable=True)
    country                           = db.Column(db.String(100), nullable=False)
    name_of_direct_supervisor         = db.Column(db.String(255), nullable=True)
    no_of_employees_supervised_by_you = db.Column(db.Integer, nullable=True)
    start_date                        = db.Column(db.Date, nullable=False)
    end_date                          = db.Column(db.Date, nullable=True)
    current                           = db.Column(db.Boolean, nullable=False, default=False)
    reason_for_leaving                = db.Column(db.String(255), nullable=True)
    reference_name                    = db.Column(db.String(255), nullable=True)
    reference_email                   = db.Column(db.String(255), nullable=True)
    reference_phone                   = db.Column(db.String(50), nullable=True)
    duties_description                = db.Column(db.Text, nullable=True)
    created_at                        = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'type_of_business': self.type_of_business,
            'name_of_employer': self.name_of_employer,
            'type_of_work': self.type_of_work,
            'address_line': self.address_line,
            'phone': self.phone,
            'fax': self.fax,
            'current_or_previous_position': self.current_or_previous_position,
            'country': self.country,
            'name_of_direct_supervisor': self.name_of_direct_supervisor,
            'no_of_employees_supervised_by_you': self.no_of_employees_supervised_by_you,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'current': self.current,
            'reason_for_leaving': self.reason_for_leaving,
            'reference': {
                'name': self.reference_name,
                'email': self.reference_email,
                'phone': self.reference_phone
            },
            'duties_description': self.duties_description,
            'created_at': self.created_at.isoformat()
        }


class Language(db.Model):
    __tablename__ = 'languages'
    id                = db.Column(db.Integer, primary_key=True)
    application_id    = db.Column(
        db.Integer, db.ForeignKey('applications.id', ondelete='CASCADE'),
        nullable=False
    )
    language          = db.Column(db.String(50), nullable=False)
    read_proficiency  = db.Column(db.String(50), nullable=False)
    write_proficiency = db.Column(db.String(50), nullable=False)
    speak_proficiency = db.Column(db.String(50), nullable=False)
    created_at        = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'language': self.language,
            'read': self.read_proficiency,
            'write': self.write_proficiency,
            'speak': self.speak_proficiency,
            'created_at': self.created_at.isoformat()
        }


class OtherInformation(db.Model):
    __tablename__ = 'other_information'
    id                          = db.Column(db.Integer, primary_key=True)
    application_id              = db.Column(
        db.Integer, db.ForeignKey('applications.id', ondelete='CASCADE'),
        nullable=False
    )
    membership_professional_bodies = db.Column(db.Text, nullable=True)
    publications_relevant_studies   = db.Column(db.Text, nullable=True)
    discharged_or_forced_to_resign  = db.Column(db.Boolean, nullable=False, default=False)
    reason_for_discharge             = db.Column(db.Text,    nullable=True)
    member_of_syndicate              = db.Column(db.Boolean, nullable=False, default=False)
    syndicate_details                = db.Column(db.Text,    nullable=True)
    has_work_practice_permit         = db.Column(db.Boolean, nullable=False, default=False)
    practice_permit_profession       = db.Column(db.Text,    nullable=True)
    created_at                       = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'membership_professional_bodies': self.membership_professional_bodies,
            'publications_relevant_studies': self.publications_relevant_studies,
            'discharged_or_forced_to_resign': self.discharged_or_forced_to_resign,
            'reason_for_discharge': self.reason_for_discharge,
            'member_of_syndicate': self.member_of_syndicate,
            'syndicate_details': self.syndicate_details,
            'has_work_practice_permit': self.has_work_practice_permit,
            'practice_permit_profession': self.practice_permit_profession,
            'created_at': self.created_at.isoformat()
        }
