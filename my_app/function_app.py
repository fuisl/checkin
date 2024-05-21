import azure.functions as func
import datetime
import json
import logging
import os

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from io import BytesIO
import base64
from qrcode import QRCode, ERROR_CORRECT_L

import pymongo
from pymongo import MongoClient

app = func.FunctionApp()

def render_qr(code):
    """Render a QR code image for given code.
    
    Args:
        code (str): The code to render.
    """

    qr = QRCode(
        version=1,
        error_correction=ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered)
    logging.info(f"QR code generated for {code}")

    return buffered.getvalue()

def html_embed(name, code):
    """Generate an HTML code to embed the QR code image.
    
    Args:
        name (str): The name of the ticket's owner.
        code (str): The code to render.
        
    Returns:
        str: The HTML email to send.
    """

    my_html = """
    <!DOCTYPE html><html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><head>
  <title> Email </title>
  <!--[if !mso]><!-- -->
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <!--<![endif]-->
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style type="text/css">
    #outlook a {
      padding: 0;
    }

    body {
      margin: 0;
      padding: 0;
      -webkit-text-size-adjust: 100%;
      -ms-text-size-adjust: 100%;
    }

    table,
    td {
      border-collapse: collapse;
      mso-table-lspace: 0pt;
      mso-table-rspace: 0pt;
    }

    img {
      border: 0;
      height: auto;
      line-height: 100%;
      outline: none;
      text-decoration: none;
      -ms-interpolation-mode: bicubic;
    }

    p {
      display: block;
      margin: 13px 0;
    }
  </style>
  <link href="https://fonts.googleapis.com/css2?family=Alata&amp;display=swap" rel="stylesheet" type="text/css" />
  <style type="text/css">
    @import url(https://fonts.googleapis.com/css2?family=Alata&amp;display=swap);
  </style>
  <!--<![endif]-->
  <style type="text/css">
    @media only screen and (min-width:480px) {
      .mj-column-per-50 {
        width: 50% !important;
        max-width: 50%;
      }

      .mj-column-per-100 {
        width: 100% !important;
        max-width: 100%;
      }
    }
  </style>
  <style type="text/css">
    @media only screen and (max-width:480px) {
      table.mj-full-width-mobile {
        width: 100% !important;
      }

      td.mj-full-width-mobile {
        width: auto !important;
      }
    }
  </style>
  <style type="text/css">
    a,
    span,
    td,
    th {
      -webkit-font-smoothing: antialiased !important;
      -moz-osx-font-smoothing: grayscale !important;
    }

    .hover:hover td,
    .hover:hover p,
    .hover:hover a {
      background-color: #d9433a !important;
    }
  </style>
</head>

<body style="background-color:#ffffff;">
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;"> Registration confirmation </div>
  <div style="background-color:#ffffff;">
    <!--[if mso | IE]>
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
    <div style="margin:0px auto;max-width:600px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
        <tbody>
          <tr>
            <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:0px;text-align:center;">
              <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
            <td
               class="" style="vertical-align:middle;width:300px;"
            >
          <![endif]-->
              <div class="mj-column-per-50 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:middle;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:middle;" width="100%">
                  <tbody><tr>
                    <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                        <tbody>
                          <tr>
                            <td style="width:150px;">
                              <a href="https://www.facebook.com/VguCareerService" target="_blank" style="color: #ea4a40; text-decoration: none;">
                              <img alt="" height="auto" src="https://vgu.edu.vn/cms-vgu-theme-4/images/cms/vgu_logo.png" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:14px;" width="150" />
                            </a>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody></table>
              </div>
              <!--[if mso | IE]>
            </td>
          
            <td
               class="" style="vertical-align:middle;width:300px;"
            >
          <![endif]-->
              <div class="mj-column-per-50 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:middle;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:middle;" width="100%">
                  <tbody><tr>
                    <td align="right" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                      <!--[if mso | IE]>
      <table
         align="right" border="0" cellpadding="0" cellspacing="0" role="presentation"
      >
        <tr>
      
              <td>
            <![endif]-->
                      <!-- <table align="right" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                        <tbody><tr>
                          <td style="padding:4px;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-radius:3px;width:18px;">
                              <tbody><tr>
                                <td style="font-size:0;height:18px;vertical-align:middle;width:18px;">
                                  <a href="#" target="_blank" style="color: #ea4a40; text-decoration: none;">
                                    <img alt="twitter-logo" height="18" src="https://codedmails.com/images/social/black/twitter-logo-transparent-black.png" style="border-radius:3px;display:block;" width="18" />
                                  </a>
                                </td>
                              </tr>
                            </tbody></table>
                          </td>
                        </tr>
                      </tbody></table> -->
                      <!--[if mso | IE]>
              </td>
            
              <td>
            <![endif]-->
                      <table align="right" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                        <tbody><tr>
                          <td style="padding:4px;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-radius:3px;width:18px;">
                              <tbody><tr>
                                <td style="font-size:0;height:18px;vertical-align:middle;width:18px;">
                                  <a href="https://www.facebook.com/VguCareerService" target="_blank" style="color: #ea4a40; text-decoration: none;">
                                    <img alt="" height="18" src="https://codedmails.com/images/social/black/facebook-logo-transparent-black.png" style="border-radius:3px;display:block;" width="18" />
                                  </a>
                                </td>
                              </tr>
                            </tbody></table>
                          </td>
                        </tr>
                      </tbody></table>
                      <!--[if mso | IE]>
              </td>
            
              <td>
            <![endif]-->
                      <!-- <table align="right" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                        <tbody><tr>
                          <td style="padding:4px;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-radius:3px;width:18px;">
                              <tbody><tr>
                                <td style="font-size:0;height:18px;vertical-align:middle;width:18px;">
                                  <a href="https://www.instagram.com/vgupresto/" target="_blank" style="color: #ea4a40; text-decoration: none;">
                                    <img alt="" height="18" src="https://codedmails.com/images/social/black/instagram-logo-transparent-black.png" style="border-radius:3px;display:block;" width="18" />
                                  </a>
                                </td>
                              </tr>
                            </tbody></table>
                          </td>
                        </tr>
                      </tbody></table> -->
                      <!--[if mso | IE]>
              </td>
            
              <td>
            <![endif]-->
                      <!-- <table align="right" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                        <tbody><tr>
                          <td style="padding:4px;">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-radius:3px;width:18px;">
                              <tbody><tr>
                                <td style="font-size:0;height:18px;vertical-align:middle;width:18px;">
                                  <a href="#" target="_blank" style="color: #ea4a40; text-decoration: none;">
                                    <img alt="instagram-logo" height="18" src="https://codedmails.com/images/social/black/linkedin-logo-transparent-black.png" style="border-radius:3px;display:block;" width="18" />
                                  </a>
                                </td>
                              </tr>
                            </tbody></table>
                          </td>
                        </tr>
                      </tbody></table> -->
                      <!--[if mso | IE]>
              </td>
            
          </tr>
        </table>
      <![endif]-->
                    </td>
                  </tr>
                </tbody></table>
              </div>
              <!--[if mso | IE]>
            </td>
          
        </tr>
      
                  </table>
                <![endif]-->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
    <div style="margin:0px auto;max-width:600px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
        <tbody>
          <tr>
            <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
              <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
            <td
               class="" style="vertical-align:top;width:600px;"
            >
          <![endif]-->
              <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                  <tbody><tr>
                    <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                        <tbody>
                          <tr>
                            <td style="width:550px;">
                              <img alt="welcome image" height="auto" src="https://scontent.fsgn2-9.fna.fbcdn.net/v/t39.30808-6/436499613_322949377495232_3738203094499996061_n.png?_nc_cat=103&ccb=1-7&_nc_sid=5f2048&_nc_ohc=PbJV3TfMHIsQ7kNvgHYtIfl&_nc_ht=scontent.fsgn2-9.fna&oh=00_AYDJjDhkHMYXn2Aja5o2JEULF8aShlLFeEdMrWDMx0YRXg&oe=664F64B2" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:14px;border-radius: 20px" width="550" />
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody></table>
              </div>
              <!--[if mso | IE]>
            </td>
          
        </tr>
      
                  </table>
                <![endif]-->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
    <div style="margin:0px auto;max-width:600px;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
        <tbody>
          <tr>
            <td style="direction:ltr;font-size:0px;padding:0 40px;text-align:center;">
              <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
            <tr>
              <td
                 class="" width="600px"
              >
          
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:520px;" width="520"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
              <div style="margin:0px auto;max-width:520px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                  <tbody>
                    <tr>
                      <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
                        <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
            <td
               class="" style="vertical-align:top;width:520px;"
            >
          <![endif]-->
                        <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tbody><tr>
                              <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <div style="font-family:Alata, sans-serif;font-size:18px;font-weight:400;line-height:24px;text-align:left;color:#000000;">
                                  <h1 style="margin: 0; font-size: 32px; line-height: 40px;">Hi [name]! <br />Thanks for joining with us.</h1>
                                </div>
                              </td>
                            </tr>
                            <tr>
                              <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <div style="font-family:Alata, sans-serif;font-size:18px;font-weight:400;line-height:24px;text-align:left;color:#000000;">
                                  <p>Your registration to Career Fair and Industry Exploration Day 2024 was <a style="color:#10962f;"> successfully completed</a>. </p>
                                  <p>Here is your ticket info: </p>
                                </div>
                              </td>
                            </tr>
                          </tbody></table>
                        </div>
                        
                        <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tbody><tr>
                              <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <div style="font-family:Alata, sans-serif;font-size:18px;font-weight:400;line-height:24px;text-align:left;color:#434245;">
                                  <p style="margin: 0;"><strong style="font-size: 14px; color: #999; line-height: 18px">When:</strong><br /> Wed, Jun 5th, 2024, 09:00 AM GMT+7</p>
                                </div>
                              </td>
                            </tr>
                            <tr>
                              <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <div style="font-family:Alata, sans-serif;font-size:18px;font-weight:400;line-height:24px;text-align:left;color:#434245;">
                                  <p style="margin: 0;"><strong style="font-size: 14px; color: #999; line-height: 18px">Where:</strong><br /> Convention Hall, VGU Campus.</p>
                                </div>
                              </td>
                            </tr>
                            <tr>
                              <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <div style="font-family:Alata, sans-serif;font-size:18px;font-weight:400;line-height:24px;text-align:left;color:#434245;">
                                  <p style="margin: 0;"><strong style="font-size: 14px; color: #999; line-height: 18px">Activities:</strong><br />Explore more on our <a href="https://www.vgu-career-fair-2024.com/student-journey" style="color: #d27024; text-decoration: none;"> website</a>.</p>
                                </div>
                              </td>
                            </tr>
                          </tbody></table>
                        </div>
                        <!--[if mso | IE]>
            </td>
          
        </tr>
      
                  </table>
                <![endif]-->
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      
              </td>
            </tr>
          
            <tr>
              <td
                 class="" width="600px"
              >
          
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:520px;" width="520"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
              <div style="margin:0px auto;max-width:520px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                  <tbody>
                    <tr>
                      <td style="direction:ltr;font-size:0px;padding:0;text-align:center;">
                        <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
            <td
               class="" style="vertical-align:top;width:520px;"
            >
          <![endif]-->
                        <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tbody><tr>
                              <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <div style="font-family:Alata, sans-serif;font-size:18px;font-weight:400;line-height:24px;text-align:left;color:#000000;">
                                  <h1 style="text-align: center; font-size: 25px; line-height: 40px;">Your entrance ticket</h1>
                                  <h1 style="text-align: center; font-size: 32px; line-height: 40px; color: #d27024">[code]</h2>
                                </div>
                              </td>
                            </tr>
                            <tr>
                              <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                                  <tbody>
                                    <tr>
                                      <td style="width:275px;">
                                        <img alt="qrcode" height="auto" src="cid:qr" style="border:0.50px #E5E5E5 solid;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:14px;border-radius: 15px" width="275" />
                                      </td>
                                    </tr>
                                  </tbody>
                                </table>
                              </td>
                            </tr>
                          </tbody></table>
                        </div>
                        <!--[if mso | IE]>
            </td>
          
        </tr>
      
                  </table>
                <![endif]-->
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      
              </td>
            </tr>
          
            <tr>
              <td
                 class="" width="600px"
              >
          
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:520px;" width="520"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
              <div style="margin:0px auto;max-width:520px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                  <tbody>
                    <tr>
                      <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                        <div style="font-family:Alata, sans-serif;font-size:18px;font-weight:400;line-height:24px;text-align:left;color:#ABABAB;">
                          <ul>
                            <li style="padding-bottom: 20px">Show this ticket at the reception desk.</li>
                            <li style="padding-bottom: 20px">Do not share this ticket to anyone.</li>
                            <li style="padding-bottom: 20px">Use the code for lucky draw.</li>
                        </div>
                      </td>
                    </tr>
                    <tr>
                    <tr>
                      <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
                        <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
            <td
               class="" style="vertical-align:top;width:520px;"
            >
          <![endif]-->
                        <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tbody><tr>
                              <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <div style="font-family:Alata, sans-serif, sans-serif;font-size:14px;font-weight:400;line-height:24px;text-align:left;color:#333333;">Have questions or need help? Email us at <a href="#" style="color: #d27024; text-decoration: none;"> careerservices@vgu.edu.vn </a></div>
                              </td>
                            </tr>
                          </tbody></table>
                        </div>
                        <!--[if mso | IE]>
            </td>
          
        </tr>
      
                  </table>
                <![endif]-->
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      
              </td>
            </tr>
          
            <tr>
              <td
                 class="" width="600px"
              >
          
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:520px;" width="520"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
              <div style="margin:0px auto;max-width:520px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                  <tbody>
                    <tr>
                      <td style="direction:ltr;font-size:0px;padding:0px;text-align:center;">
                        <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
            <td
               class="" style="vertical-align:top;width:520px;"
            >
          <![endif]-->
                        <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tbody><tr>
                              <td style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <p style="border-top:solid 1px #f4f4f4;font-size:1px;margin:0px auto;width:100%;">
                                </p>
                                <!--[if mso | IE]>
        <table
           align="center" border="0" cellpadding="0" cellspacing="0" style="border-top:solid 1px #f4f4f4;font-size:1px;margin:0px auto;width:470px;" role="presentation" width="470px"
        >
          <tr>
            <td style="height:0;line-height:0;">
              &nbsp;
            </td>
          </tr>
        </table>
      <![endif]-->
                              </td>
                            </tr>
                            <tr>
                              <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <div style="font-family:Alata, sans-serif;font-size:14px;font-weight:400;line-height:24px;text-align:center;color:#333333;">OwO to the WoW!</div>
                              </td>
                            </tr>
                            <tr>
                              <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <!--[if mso | IE]>
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
      >
        <tr>
      
              <td>
            <![endif]-->
                                <!--[if mso | IE]>
              </td>
            
              <td>
            <![endif]-->
                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                                  <tbody><tr>
                                    <td style="padding:4px;">
                                      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-radius:3px;width:24px;">
                                        <tbody><tr>
                                          <td style="font-size:0;height:24px;vertical-align:middle;width:24px;">
                                            <a href="https://www.facebook.com/VguCareerService" target="_blank" style="color: #ea4a40; text-decoration: none;">
                                              <img alt="facebook-logo" height="24" src="https://codedmails.com/images/social/black/facebook-logo-transparent-black.png" style="border-radius:3px;display:block;" width="24" />
                                            </a>
                                          </td>
                                        </tr>
                                      </tbody></table>
                                    </td>
                                  </tr>
                                </tbody></table>
                                <!--[if mso | IE]>
              </td>
            
              <td>
            <![endif]-->
                                <!-- <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table;">
                                  <tbody><tr>
                                    <td style="padding:4px;">
                                      <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-radius:3px;width:24px;">
                                        <tbody><tr>
                                          <td style="font-size:0;height:24px;vertical-align:middle;width:24px;">
                                            <a href="https://www.instagram.com/vgupresto/" target="_blank" style="color: #ea4a40; text-decoration: none;">
                                              <img alt="instagram-logo" height="24" src="https://codedmails.com/images/social/black/instagram-logo-transparent-black.png" style="border-radius:3px;display:block;" width="24" />
                                            </a>
                                          </td>
                                        </tr>
                                      </tbody></table>
                                    </td>
                                  </tr>
                                </tbody></table> -->
                                <!--[if mso | IE]>
              </td>
            
              <td>
            <![endif]-->
                                <!--[if mso | IE]>
              </td>
            
          </tr>
        </table>
      <![endif]-->
                              </td>
                            </tr>
                            <tr>
                              <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <div style="font-family:Alata, sans-serif;font-size:14px;font-weight:400;line-height:24px;text-align:center;color:#333333;">Vanh Dai 4 St., Thoi Hoa Ward, Ben Cat, Binh Duong<br /> ©2024 VGU CAREER SERVICE.</div>
                              </td>
                            </tr>
                            <!-- <tr>
                              <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                                  <tbody>
                                    <tr>
                                      <td style="width:50px;">
                                        <img alt="image description" height="auto" src="assets/logopresto.jpg" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:14px;" width="50" />
                                      </td>
                                    </tr>
                                  </tbody>
                                </table>
                              </td>
                            </tr> -->
                          </tbody></table>
                        </div>
                        <!--[if mso | IE]>
            </td>
          
        </tr>
      
                  </table>
                <![endif]-->
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      
              </td>
            </tr>
          
            <tr>
              <td
                 class="" width="600px"
              >
          
      <table
         align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:520px;" width="520"
      >
        <tr>
          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
      <![endif]-->
              <div style="margin:0px auto;max-width:520px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                  <tbody>
                    <tr>
                      <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;">
                        <!--[if mso | IE]>
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                
        <tr>
      
            <td
               class="" style="vertical-align:top;width:520px;"
            >
          <![endif]-->
                        <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                            <tbody><tr>
                              <td style="font-size:0px;word-break:break-word;">
                                <!--[if mso | IE]>
    
        <table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td height="1" style="vertical-align:top;height:1px;">
      
    <![endif]-->
                                <div style="height:1px;">   </div>
                                <!--[if mso | IE]>
    
        </td></tr></table>
      
    <![endif]-->
                              </td>
                            </tr>
                          </tbody></table>
                        </div>
                        <!--[if mso | IE]>
            </td>
          
        </tr>
      
                  </table>
                <![endif]-->
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      
              </td>
            </tr>
          
                  </table>
                <![endif]-->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!--[if mso | IE]>
          </td>
        </tr>
      </table>
      <![endif]-->
  </div>


</body></html>
    """
    # with open("email_template.html", "r") as f:
    #     my_html = f.read()

    my_html = my_html.replace("[name]", name)\
                        .replace("[code]", code)
    
    return my_html

def send_email(code, name, email):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.ehlo()
    server.login(os.environ["EMAIL"], os.environ["EMAIL_PASSWORD"])
    logging.info("Logging status: " + str(server.noop()))

    msg = MIMEMultipart()
    msg['From'] = os.environ["EMAIL"]
    msg['To'] = email
    msg['Subject'] = "CFIED 2024 Registration Confirmation"

    content = html_embed(name=name, code=code)
    msg.attach(MIMEText(content, 'html'))

    logging.info("QR code generation...")
    img_str = render_qr(code)
    logging.info("QR code generated.")

    img = MIMEImage(img_str, name="qr.png")
    img.add_header('Content-ID', 'qr')
    msg.attach(img)

    server.sendmail(os.environ["EMAIL"], email, msg.as_string())
    server.quit()
    logging.info("Email sent to: " + email + " successfully.")

@app.route(route="career_qr", auth_level=func.AuthLevel.ADMIN)
def career_qr(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    name = req.params.get('name')
    email = req.params.get('email')

    if not name or not email:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
            email = req_body.get('email')

    if not name:
        name = req.headers.get('name')
    if not email:
        email = req.headers.get('email')


    if not name or not email:
        data = req_body.get('data')
        # logging.info(f"Data: {data}")
        if data:
            name = data['contact']['name']['first']
            email = data['contact']['email']

    logging.info(f"Name: {name}, Email: {email}")

    if not name or not email:
        return func.HttpResponse(
             "Please pass a name and email on the query string or in the request body",
             status_code=400
        )
    
    # save to db
    connection_uri = os.environ["MONGO_URI"]
    client = MongoClient(connection_uri)
    db = client["vgu"]
    collection = db["career_fair"]

    existing_data = collection.find_one({"email": email})

    logging.info(f"Existing data: {existing_data}")

    if existing_data:
      collection.update_one({"email": email}, {"$set": {"name": name}})
      logging.info(f"Updated data with email: {email}")
      obj_id_str = str(existing_data["_id"])
      code = existing_data["code"]
      name = existing_data["name"]
    else:
      data = {
        "name": name,
        "email": email
      }
      obj_id = collection.insert_one(data).inserted_id
      obj_id_str = str(obj_id)

      # get 6 last characters of obj_id as code and update
      code = str(int(obj_id_str[-6:], 16)%1000000)
      collection.update_one({"_id": obj_id}, {"$set": {"code": code}})
      logging.info(f"Inserted data with id: {obj_id_str}")

    logging.info(f"Code: {code}")
    send_email(code, name, email)

    return func.HttpResponse(f"Data inserted with id: {obj_id_str}. Email sent to {email}.", status_code=200)