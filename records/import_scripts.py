"""
I am really sorry for this giant mess of a file
Across the many times I have had to import data into the database,
this is the file I have used.
Hopefully gives you a good idea of what needs to be done
while importing. DO make a tool for this for django-admin or sth
"""

import csv
import re
from collections import OrderedDict
from .models import Student, FurtherAcademicStatus, Address

from django.contrib.auth.models import User

import datetime
from nepali_date import NepaliDate

from django.core.files import File

from django.db import IntegrityError

user_username = 'csv-importer'
user_password = 'csv-importer'

level_be = 'be'
level_msc = 'msc'
level_phd = 'phd'

month_name_num_dict = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
}

ordered_fieldnames = OrderedDict([
    ('title', None),
    ('first_name', None),
    ('middle_name', None),
    ('last_name', None),
    ('fathers_name', None),
    ('mothers_name', None),
    ('be_program', None),
    ('be_program_type', None),
    ('be_batch_bs', None),
    ('be_roll_number', None),
    ('be_ioe_roll_number', None),
    ('be_student_group', None),
    ('msc_program', None),
    ('msc_program_type', None),
    ('msc_batch_bs', None),
    ('msc_roll_number', None),
    ('msc_ioe_roll_number', None),
    ('phd_program_type', None),
    ('phd_batch_bs', None),
    ('phd_roll_number', None),
    ('phd_ioe_roll_number', None),
    ('contact_number', None),
    ('email', None),
    ('website', None),
    ('facebook_id', None),
    ('twitter_id', None),
    ('linked_in_id', None),
    ('areas_of_expertise', None),
    ('dob_bs', None),
    ('gender', None),
    ('employment_status', None),
    ('currently_employed_organization', None),
    ('current_post_in_organization', None),
    ('address_type', None),
    ('country', None),
    ('state', None),
    ('district', None),
    ('city', None),
    ('vdc_municipality', None),
    ('ward_no', None),
    ('level', None),
    ('status', None),
    ('details', None),
])

ordered_fieldnames_student = [
    'title',
    'first_name',
    'middle_name',
    'last_name',
    'fathers_name',
    'mothers_name',
    'be_program',
    'be_program_type',
    'be_batch_bs',
    'be_roll_number',
    'be_ioe_roll_number',
    'be_student_group',
    'msc_program',
    'msc_program_type',
    'msc_batch_bs',
    'msc_roll_number',
    'msc_ioe_roll_number',
    'phd_batch_bs',
    'phd_program_type',
    'phd_roll_number',
    'phd_ioe_roll_number',
    'contact_number',
    'email',
    'website',
    'facebook_id',
    'twitter_id',
    'linked_in_id',
    'areas_of_expertise',
    'dob_bs',
    'gender',
    'employment_status',
    'currently_employed_organization',
    'current_post_in_organization',
]

ordered_fieldnames_address = [
    'address_type',
    'country',
    'state',
    'district',
    'city',
    'vdc_municipality',
    'ward_no',
]

ordered_fieldnames_academic_status = [
    'level',
    'status',
    'details',
]


def parse_date_string_doece_ad(unparsed):
    #AD dates of the format 14-Apr-83
    # 12-Nov-93  12-Nov-93
    if re.search("^[0-9]*-[a-zA-Z]{3}-[0-9]{2}$", unparsed):
        day, month, year = unparsed.split('-')
        day = int(day)
        month = month_name_num_dict[month]
        year = int('19'+year)
        dob_ad = datetime.date(year, month, day)
        dob_bs = NepaliDate.to_nepali_date(dob_ad)
        year = str(dob_bs.year)
        month = str(dob_bs.month)
        if len(month) == 1:
            month = '0'+month
        day = str(dob_bs.day)
        if len(day) == 1:
            day = '0'+day
        return f'{year}/{month}/{day}'
    else:
        return f'null_value'


def parse_roll_num_doece(unparsed, batch_bs='0000', program='XXX'):
    """
    \
    :param unparsed:
           batch_bs: e.g. 2055
           program: e.g. BCT
    :return: tuple of (batch_bs, program, roll_number)
    """
    if re.search("^20[0-9]{2}/[A-Z]{3}/[0-9]{3}$", unparsed):
        batch_bs, program, roll_number = unparsed.split('/')
        return batch_bs, program, roll_number
    elif re.search('^[0-9]{3}$', unparsed):
        roll_number = unparsed
        return batch_bs, program, roll_number
    elif re.search('[0-9]{3}[A-Z]+[0-9]{3}$', unparsed):
        batch_bs = f'2{unparsed[:3]}'
        roll_number = unparsed[-3:]
        return batch_bs, program, roll_number
    else:
        return None, None, None


def parse_date_string(unparsed):
    # handles following 4 conditions
    # 2058-02-30
    # 17-10-50
    # 5/3/1957 should be 2057 actually
    if re.search("^20[0-9]{2}-[0-9]{2}-[0-9]{2}$", unparsed):
        year, month, day = unparsed.split('-')
        return f'{year}/{month}/{day}'
    elif re.search("^[0-9]{2}-[0-9]{2}-[0-9]{2}$", unparsed):
        day, month, year = unparsed.split('-')
        return f'20{year}/{month}/{day}'
    elif re.search("^[0-9]+/[0-9]+/[0-9]+$", unparsed):
        month, day, year = unparsed.split('/')
        if len(day) == 1:
            day = '0'+day
        if len(month) == 1:
            month = '0'+month
        year = '20'+year[-2:]
        return f'{year}/{month}/{day}'
    else:
        return f'null_value'


def import_clean_data(clean_file_name, user):
    with open(clean_file_name) as csv_in_file:
        csv_reader = csv.DictReader(csv_in_file, delimiter=",")
        line_count=0
        for row in csv_reader:
            if line_count==0:
                print(f'Column names are {", ".join(row)}')
                field_names = row
                line_count += 1
            temp_stu = Student.objects.create(uploader=user)
            for field in ordered_fieldnames_student:
                if row[field]:
                    setattr(temp_stu, field, row[field])
            if row['country']:
                temp_addr = Address.objects.create(student=temp_stu)
                for field in ordered_fieldnames_address:
                    if row[field]:
                        setattr(temp_addr, field, row[field])
                temp_addr.save()
            if row['level']:
                temp_acad = FurtherAcademicStatus.objects.create(student=temp_stu)
                for field in ordered_fieldnames_academic_status:
                    if row[field]:
                        setattr(temp_acad, field, row[field])
                temp_acad.save()
            try:
                temp_stu.save()
            except IntegrityError as e:
                print(f"IntegrityError = e {str(e)}")
            line_count += 1
        print(f'{line_count-1} records entered into db!')


def clean_cit_data(in_file_name, out_file_name, level):
    with open(in_file_name) as csv_in_file, open(out_file_name, "w", newline='') as csv_out_file:

        csv_reader = csv.DictReader(csv_in_file, delimiter=",")

        csv_writer = csv.DictWriter(csv_out_file, fieldnames=ordered_fieldnames)
        csv_writer.writeheader()

        line_count=0
        for row in csv_reader:
            if line_count==0:
                print(f'Column names are {", ".join(row)}')
                field_names = row
                line_count += 1
            new_row = {}
            roll_number = row["classRollNo"]
            match = re.search("^([0-9]+)([A-Z]+)([0-9]+)$", roll_number)
            new_row[f'{level}_program'] = match.group(2)
            new_row[f'{level}_batch_bs'] = f'2{match.group(1)[-3:]}'
            new_row[f'{level}_roll_number'] = match.group(3)
            new_row[f'{level}_program_type'] = row['programType']
            new_row['be_student_group'] = row['studentGroup']
            if row['uniqueRollNo']:
                new_row[f'{level}_ioe_roll_number'] = row['uniqueRollNo']

            if row['lastName']:
                new_row[f'first_name'] = row['firstName']
                new_row[f'middle_name'] = row['middleName']
                new_row[f'last_name'] = row['lastName']
            else:
                *first, last = row['firstName'].split(" ")
                first = ' '.join(first)
                new_row[f'first_name'] = first
                new_row[f'last_name'] = last

            dob_str = row['dobBs']
            parsed_dob_str = parse_date_string(dob_str)
            # print(f'{dob_str} becomes {parsed_dob_str}')
            if parsed_dob_str != 'null_value':
                new_row['dob_bs'] = parsed_dob_str

            if row['gender']:
                new_row['gender'] = row['gender']

            if row['fatherName']:
                new_row['fathers_name'] = row['fatherName']
            if row['motherName']:
                new_row['mothers_name'] = row['motherName']

            if row['mobileNo']:
                new_row['contact_number'] = row['mobileNo']

            new_row['email'] = row['emailId']

            country_name = row['countryName']
            if row['countryName']:
                new_row['address_type'] = 'Permanent'
            if country_name == "Nepal":
                new_row['country'] = "NP"
            elif country_name == "India":
                new_row['country'] = "IN"
            else:
                print(f'{country_name} country not read for with date {dob_str}')

            new_row['district'] = row['district']
            new_row['vdc_municipality'] = row['vdcMuncipal']
            new_row['ward_no'] = row['wardNo']
            csv_writer.writerow(new_row)

            line_count += 1
        print(f'{line_count} records read!')


def clean_doece_data(in_file_name, out_file_name, level, batch_bs, program):
    with open(in_file_name) as csv_in_file, open(out_file_name, "w", newline='') as csv_out_file:

        csv_reader = csv.DictReader(csv_in_file, delimiter=",")

        csv_writer = csv.DictWriter(csv_out_file, fieldnames=ordered_fieldnames)
        csv_writer.writeheader()

        line_count=0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                field_names = row
                line_count += 1
            new_row = {}
            unparsed_roll_number = row["Roll No"]
            batch_bs, program, roll_number = parse_roll_num_doece(unparsed_roll_number, batch_bs, program)
            if not roll_number:
                continue
            new_row[f'{level}_program'] = program
            new_row[f'{level}_batch_bs'] = batch_bs
            new_row[f'{level}_roll_number'] = roll_number
            if row['IOEROllNo']:
                new_row[f'{level}_ioe_roll_number'] = row['IOEROllNo']

            new_row[f'first_name'] = row['First Name']
            new_row[f'middle_name'] = row['Middle Name']
            new_row[f'last_name'] = row['Last Name']

            new_row[f'{level}_program_type'] = row['ProgramType']

            dob_str = row['DOB']
            parsed_dob_str = parse_date_string_doece_ad(dob_str)
            # print(f'{dob_str} becomes {parsed_dob_str}')
            if parsed_dob_str != 'null_value':
                new_row['dob_bs'] = parsed_dob_str

            if row['Gender']:
                if row['Gender'] == 'M':
                    new_row['gender'] = 'Male'
                else:
                    new_row['gender'] = 'Female'

            if row['Phone']:
                new_row['contact_number'] = row['Phone']

            if row['district']:
                new_row['address_type'] = 'Permanent'
                new_row['country'] = "NP"
                new_row['district'] = row['district']
                new_row['vdc_municipality'] = row['vdcMuncipal']
                new_row['ward_no'] = row['wardNo']

            new_row['email'] = row['Email']

            csv_writer.writerow(new_row)

            line_count += 1
        print(f'{line_count-1} records read!')


def import_cit_data(source_filename, clean_filename, level):
    user = User.objects.get(username=user_username)
    clean_cit_data(f"D:\\Users\\super\\PycharmProjects\\DOECEAlumniStudent\\data\\orig\\{source_filename}",
                   f"D:\\Users\\super\\PycharmProjects\\DOECEAlumniStudent\\data\\clean\\{clean_filename}",
                   level
                   )
    import_clean_data(f"D:\\Users\\super\\PycharmProjects\\DOECEAlumniStudent\\data\\clean\\{clean_filename}", user)


def import_doece_data(source_filename, clean_filename, level, batch_bs, program):
    user = User.objects.get(username=user_username)
    # clean_doece_data(f"D:\\Users\\super\\PycharmProjects\\DOECEAlumniStudent\\data\\orig\\{source_filename}",
    #                  f"D:\\Users\\super\\PycharmProjects\\DOECEAlumniStudent\\data\\clean\\{clean_filename}",
    #                  level,
    #                  batch_bs,
    #                  program,
    #                  )
    import_clean_data(f"/home/bob/DoeceAlumniStudentPortal/data/clean/{clean_filename}", user)


def import_picture_cit_data(filename_path):
    # with open(filename_path) as file:
    #     Student.objects.filter()
    #     csv_reader = csv.DictReader(csv_in_file, delimiter=",")
    #     line_count = 0
    #     for row in csv_reader:
    #         if line_count == 0:
    #             print(f'Column names are {", ".join(row)}')
    #             field_names = row
    #             line_count += 1
    #         temp_stu = Student.objects.create(uploader=user)
    #         for field in ordered_fieldnames_student:
    #             if row[field]:
    #                 setattr(temp_stu, field, row[field])
    #         if row['country']:
    #             temp_addr = Address.objects.create(student=temp_stu)
    #             for field in ordered_fieldnames_address:
    #                 if row[field]:
    #                     setattr(temp_addr, field, row[field])
    #             temp_addr.save()
    #         if row['level']:
    #             temp_acad = FurtherAcademicStatus.objects.create(student=temp_stu)
    #             for field in ordered_fieldnames_academic_status:
    #                 if row[field]:
    #                     setattr(temp_acad, field, row[field])
    #             temp_acad.save()
    #         try:
    #             temp_stu.save()
    #         except IntegrityError as e:
    #             print(f"IntegrityError = e {str(e)}")
    #         line_count += 1
    #     print(f'{line_count - 1} records entered into db!')
    pass

def main():
    # for program in ['BCT', 'BEX', 'BEI']:
    #     import_cit_data(f"{program}.csv", f"{program}_clean.csv", level=level_be)
    #
    # for program in ['MSCSK']:
    #     for batch in range(69, 75):
    #         import_doece_data(
    #             source_filename=f'0{batch}MSCS.csv',
    #             clean_filename=f'0{batch}{program}_clean.csv',
    #             level=level_msc,
    #             batch_bs=f'20{batch}',
    #             program=program
    #         )

    # for program in ['BEX']:
    #     for batch in range(51, 55):
    #         import_doece_data(
    #             source_filename=f'{program}0{batch}.csv',
    #             clean_filename=f'{program}0{batch}_clean.csv',
    #             level=level_be,
    #             batch_bs=f'20{batch}',
    #             program=program
    #         )
    num_added = 0
    num_total = 0
    # program = "bct"
    # for batch in ['059', '060', '061', '062', '063', '064', '065', '066', '067', '068',]:
    #     for format in ['.jpg',]:
    #         for roll_number in range(501, 560):
    #             roll_number = str(roll_number)
    #             filename_path = "cit_pictures/" + batch + program + roll_number + format
    #             filename = batch + program + roll_number + format
    #             try:
    #                 with open(filename_path, 'rb') as file:
    #                     num_total += 1
    #                     if (not len(Student.objects.filter(
    #                             be_batch_bs__exact=f'2{batch}',
    #                             be_program__exact=program.upper(),
    #                             be_roll_number__exact=roll_number,
    #                     )) == 1):
    #                         print(f'More than one record for {filename_path}')
    #                     else:
    #                         student = Student.objects.filter(
    #                             be_batch_bs__exact=f'2{batch}',
    #                             be_program__exact=program.upper(),
    #                             be_roll_number__exact=roll_number,
    #                         ).first()
    #                         if (not student.recent_passport_size_photo):
    #                             print("No photo yet")
    #                             # student.recent_passport_size_photo = File(file)
    #                             student.recent_passport_size_photo.save(filename, File(file))
    #                             # e.license_file.save(new_name, ContentFile('A string with the file content'))
    #                             student.save()
    #                             num_added += 1
    #                         else:
    #                             print("Photo already added")
    #             except IOError as e:
    #                 print("Couldn't open or write to file (%s)." % e)
    # program = "bct"
    # for batch in ['064', '067', '068',]:
    #     for format in ['.jpg',]:
    #         for roll_number in range(401, 460):
    #             correct_roll_number = str(roll_number+100)
    #             roll_number = str(roll_number)
    #             filename_path = "cit_pictures/" + batch + program + roll_number + format
    #             filename = batch + program + correct_roll_number + format
    #             try:
    #                 with open(filename_path, 'rb') as file:
    #                     num_total += 1
    #                     if (not len(Student.objects.filter(
    #                             be_batch_bs__exact=f'2{batch}',
    #                             be_program__exact=program.upper(),
    #                             be_roll_number__exact=correct_roll_number,
    #                     )) == 1):
    #                         print(f'More than one record for {filename_path}')
    #                     else:
    #                         student = Student.objects.filter(
    #                             be_batch_bs__exact=f'2{batch}',
    #                             be_program__exact=program.upper(),
    #                             be_roll_number__exact=correct_roll_number,
    #                         ).first()
    #                         if (not student.recent_passport_size_photo):
    #                             print("No photo yet")
    #                             # student.recent_passport_size_photo = File(file)
    #                             student.recent_passport_size_photo.save(filename, File(file))
    #                             # e.license_file.save(new_name, ContentFile('A string with the file content'))
    #                             student.save()
    #                             num_added += 1
    #                         else:
    #                             print("Photo already added")
    #             except IOError as e:
    #                 print("Couldn't open or write to file (%s)." % e)
    #
    # program="bex"
    # for batch in ['059', '060', '061', '062', '063', '064', '065', '066', '067', '068', ]:
    #     for format in ['.jpg',]:
    #         for roll_number in range(401, 460):
    #             roll_number = str(roll_number)
    #             filename_path = "cit_pictures/"+batch+program+roll_number+format
    #             filename = batch+program+roll_number+format
    #             try:
    #                  with open(filename_path, 'rb') as file:
    #                     num_total += 1
    #                     if(not len(Student.objects.filter(
    #                         be_batch_bs__exact=f'2{batch}',
    #                         be_program__exact=program.upper(),
    #                         be_roll_number__exact=roll_number,
    #                     )) == 1):
    #                         print(f'More than one record for {filename_path}')
    #                     else:
    #                         student = Student.objects.filter(
    #                                 be_batch_bs__exact=f'2{batch}',
    #                                 be_program__exact=program.upper(),
    #                                 be_roll_number__exact=roll_number,
    #                             ).first()
    #                         if(not student.recent_passport_size_photo):
    #                             print("No photo yet")
    #                             # student.recent_passport_size_photo = File(file)
    #                             student.recent_passport_size_photo.save(filename, File(file))
    #                             # e.license_file.save(new_name, ContentFile('A string with the file content'))
    #                             student.save()
    #                             num_added+=1
    #                         else:
    #                             print("Photo already added")
    #             except IOError as e:
    #                 print("Couldn't open or write to file (%s)." % e)
    # print(f'{num_added} added out of {num_total}')
    program = "msic"
    for batch in ['073',]:
        for format in ['.jpg', '.png']:
            for roll_number in range(601, 623):
                roll_number = str(roll_number)
                filename_path = "cit_pictures/" + batch + program + roll_number + format
                filename = batch + program + roll_number + format
                try:
                    with open(filename_path, 'rb') as file:
                        num_total += 1
                        if (not len(Student.objects.filter(
                                msc_batch_bs__exact=f'2{batch}',
                                msc_program__exact="MSICE",
                                msc_roll_number__exact=roll_number,
                        )) == 1):
                            print(f'More than one record for {filename_path}')
                        else:
                            student = Student.objects.filter(
                                msc_batch_bs__exact=f'2{batch}',
                                msc_program__exact="MSICE",
                                msc_roll_number__exact=roll_number,
                            ).first()
                            if (not student.recent_passport_size_photo):
                                print("No photo yet")
                                # student.recent_passport_size_photo = File(file)
                                student.recent_passport_size_photo.save(filename, File(file))
                                # e.license_file.save(new_name, ContentFile('A string with the file content'))
                                student.save()
                                num_added += 1
                            else:
                                print("Photo already added")
                except IOError as e:
                    print("Couldn't open or write to file (%s)." % e)
    program = "msice"
    for batch in ['074', ]:
        for format in ['.jpg', '.png']:
            for roll_num in range(0, 23):
                if roll_num < 10:
                    roll_number = f'00{roll_num}'
                else:
                    roll_number = f'0{roll_num}'
                roll_number = str(roll_number)
                filename_path = "cit_pictures/" + batch + program + roll_number + format
                filename = batch + program + roll_number + format
                try:
                    with open(filename_path, 'rb') as file:
                        num_total += 1
                        if (not len(Student.objects.filter(
                                msc_batch_bs__exact=f'2{batch}',
                                msc_program__exact="MSICE",
                                msc_roll_number__exact=roll_number,
                        )) == 1):
                            print(f'More than one record for {filename_path}')
                        else:
                            student = Student.objects.filter(
                                msc_batch_bs__exact=f'2{batch}',
                                msc_program__exact="MSICE",
                                msc_roll_number__exact=roll_number,
                            ).first()
                            if (not student.recent_passport_size_photo):
                                print("No photo yet")
                                # student.recent_passport_size_photo = File(file)
                                student.recent_passport_size_photo.save(filename, File(file))
                                # e.license_file.save(new_name, ContentFile('A string with the file content'))
                                student.save()
                                num_added += 1
                            else:
                                print("Photo already added")
                except IOError as e:
                    print("Couldn't open or write to file (%s)." % e)

    program = "mscs"
    for batch in ['073',]:
        for format in ['.jpg', '.png']:
            for roll_number in range(651, 673):
                roll_number = str(roll_number)
                filename_path = "cit_pictures/" + batch + program + roll_number + format
                filename = batch + program + roll_number + format
                try:
                    with open(filename_path, 'rb') as file:
                        num_total += 1
                        if (not len(Student.objects.filter(
                                msc_batch_bs__exact=f'2{batch}',
                                msc_program__exact='MSCSK',
                                msc_roll_number__exact=roll_number,
                        )) == 1):
                            print(f'More than one record for {filename_path}')
                        else:
                            student = Student.objects.filter(
                                msc_batch_bs__exact=f'2{batch}',
                                msc_program__exact='MSCSK',
                                msc_roll_number__exact=roll_number,
                            ).first()
                            if (not student.recent_passport_size_photo):
                                print("No photo yet")
                                # student.recent_passport_size_photo = File(file)
                                student.recent_passport_size_photo.save(filename, File(file))
                                # e.license_file.save(new_name, ContentFile('A string with the file content'))
                                student.save()
                                num_added += 1
                            else:
                                print("Photo already added")
                except IOError as e:
                    print("Couldn't open or write to file (%s)." % e)
    program = "mscsk"
    for batch in ['074', ]:
        for format in ['.jpg', '.png']:
            for roll_num in range(0, 23):
                if roll_num < 10:
                    roll_number = f'00{roll_num}'
                else:
                    roll_number = f'0{roll_num}'
                roll_number = str(roll_number)
                filename_path = "cit_pictures/" + batch + program + roll_number + format
                filename = batch + program + roll_number + format
                try:
                    with open(filename_path, 'rb') as file:
                        num_total += 1
                        if (not len(Student.objects.filter(
                                msc_batch_bs__exact=f'2{batch}',
                                msc_program__exact='MSCSK',
                                msc_roll_number__exact=roll_number,
                        )) == 1):
                            print(f'More than one record for {filename_path}')
                        else:
                            student = Student.objects.filter(
                                msc_batch_bs__exact=f'2{batch}',
                                msc_program__exact='MSCSK',
                                msc_roll_number__exact=roll_number,
                            ).first()
                            if (not student.recent_passport_size_photo):
                                print("No photo yet")
                                # student.recent_passport_size_photo = File(file)
                                student.recent_passport_size_photo.save(filename, File(file))
                                # e.license_file.save(new_name, ContentFile('A string with the file content'))
                                student.save()
                                num_added += 1
                            else:
                                print("Photo already added")
                except IOError as e:
                    print("Couldn't open or write to file (%s)." % e)
    print(f'{num_added} added out of {num_total}')
    # program = "bct"
    # for batch in ['071']:
    #     for format in ['.gif']:
    #         for roll_number in range(520, 521):
    #             roll_number = str(roll_number)
    #             filename_path = "cit_pictures/" + batch + program + roll_number + format
    #             filename = batch + program + roll_number + format
    #             try:
    #                 with open(filename_path, 'rb') as file:
    #                     num_total += 1
    #                     if (not len(Student.objects.filter(
    #                             be_batch_bs__exact=f'2{batch}',
    #                             be_program__exact=program.upper(),
    #                             be_roll_number__exact=roll_number,
    #                     )) == 1):
    #                         print(f'More than one record for {filename_path}')
    #                     else:
    #                         student = Student.objects.filter(
    #                             be_batch_bs__exact=f'2{batch}',
    #                             be_program__exact=program.upper(),
    #                             be_roll_number__exact=roll_number,
    #                         ).first()
    #                         if (not student.recent_passport_size_photo):
    #                             print("No photo yet")
    #                             # student.recent_passport_size_photo = File(file)
    #                             student.recent_passport_size_photo.save(filename, File(file))
    #                             # e.license_file.save(new_name, ContentFile('A string with the file content'))
    #                             student.save()
    #                             num_added += 1
    #                         else:
    #                             print("Photo already added")
    #             except IOError as e:
    #                 print("Couldn't open or write to file (%s)." % e)

if __name__=="__main__":
    main()
