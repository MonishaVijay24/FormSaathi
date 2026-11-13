import type { FormField, ProfileField, SupportingDocument } from "../types";
const f = (field_id:string,label_original:string,en:string,kn:string,data_type:FormField["data_type"],group:string,o:Partial<FormField>={}):FormField=>({field_id,label_original,label_simple:{en,kn},data_type,group,required:true,sensitive:false,confidence:0.95,...o});
export const BANK_FIELDS: FormField[] = [
 f("applicant_name","Applicant Name","Please tell me your full name.","ನಿಮ್ಮ ಪೂರ್ಣ ಹೆಸರನ್ನು ಹೇಳಿ.","text","Personal Details"),
 f("dob","DOB","Enter your date of birth (DD/MM/YYYY).","ನಿಮ್ಮ ಜನ್ಮ ದಿನಾಂಕ ಹೇಳಿ (ದಿನ/ತಿಂಗಳು/ವರ್ಷ).","date","Personal Details"),
 f("mobile","Mobile No.","Enter your 10-digit mobile number.","ನಿಮ್ಮ 10 ಅಂಕಿಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ.","number","Personal Details",{sensitive:true,digits:true}),
 f("address_permanent","Permanent Address","Your permanent home address.","ನಿಮ್ಮ ಶಾಶ್ವತ ವಿಳಾಸ.","address","Permanent / Home Address"),
 f("occupation","Occupation","What work do you do?","ನೀವು ಯಾವ ಕೆಲಸ ಮಾಡುತ್ತೀರಿ?","text","Occupation and Income"),
 f("annual_income","Annual Income","How much do you earn yearly (in rupees)?","ನೀವು ವರ್ಷಕ್ಕೆ ಎಷ್ಟು ಗಳಿಸುತ್ತೀರಿ?","number","Occupation and Income",{confidence:0.7}),
 f("account_number","Account No.","Account number printed in your passbook.","ಪಾಸ್‌ಬುಕ್‌ನಲ್ಲಿರುವ ಖಾತೆ ಸಂಖ್ಯೆ.","number","Bank Details",{sensitive:true,digits:true}),
 f("ifsc","IFSC","Bank branch code (11 characters, e.g. DEMO0001234).","ಬ್ಯಾಂಕ್ ಶಾಖೆಯ ಕೋಡ್ (11 ಅಕ್ಷರ).","text","Bank Details"),
];
export const MOCK_PROFILE: ProfileField[] = [
 {key:"name",label:"Full Name",value:"Ananya Rao",masked:false,source:"Sample Aadhaar (SAMPLE)",confidence:0.97,confirmed:false},
 {key:"dob",label:"Date of Birth",value:"15/04/2002",masked:false,source:"Sample Aadhaar (SAMPLE)",confidence:0.96,confirmed:false},
 {key:"address",label:"Address",value:"Sample address, Bengaluru",masked:false,source:"Sample Aadhaar (SAMPLE)",confidence:0.78,confirmed:false},
 {key:"id",label:"ID Reference",value:"XXXX XXXX 1234",masked:true,source:"Sample Aadhaar (SAMPLE)",confidence:0.99,confirmed:false},
];
export const MOCK_DOCS: SupportingDocument[] = [
 {id:"identity",title:"Identity document",uploaded:true,filename:"sample_aadhaar.pdf",values:{name:"Ananya R.",dob:"15/04/2002"},confidence:0.9},
 {id:"income",title:"Income certificate",uploaded:false,values:{income:"180000"},confidence:0.92},
 {id:"marks",title:"Marks card",uploaded:false,values:{percentage:"84%"},confidence:0.9},
 {id:"passbook",title:"Bank passbook",uploaded:false,values:{ifsc:"DEMO0001234"},confidence:0.93},
];
