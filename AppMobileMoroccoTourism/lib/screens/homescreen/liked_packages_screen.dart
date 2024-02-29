import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import '../../resources/color.dart';
import 'dart:convert';



class LikedPackagesScreen extends StatefulWidget {
  const LikedPackagesScreen({Key? key}) : super(key: key);

  @override
  State<LikedPackagesScreen> createState() => _LikedPackagesScreenState();
}

class _LikedPackagesScreenState extends State<LikedPackagesScreen> {

  String predictionResult = 'Hi, how can I help you?';
  TextEditingController _textController = TextEditingController();
  String selectedLanguage = 'Darija to English';

  List<String> languages = ['Darija to English', 'English to Darija', 'Assistant Trans'];

  Future<void> _sendText() async {
    String text = _textController.text;
    if (text.isNotEmpty) {
      setState(() {
        predictionResult = 'Sending text...';
      });

      sendTextAndGetResult(text, selectedLanguage).then((result) {
        setState(() {
          predictionResult = result;
        });
      }).catchError((error) {
        setState(() {
          predictionResult = 'Error sending text: $error';
        });
      });
    } else {
      setState(() {
        predictionResult = 'Please enter some text';
      });
    }
  }


  Future<String> sendTextAndGetResult(String text, String language) async {
    late String url;

    try {
      if (language == 'Darija to English') {
        url = 'http://100.91.176.36:3000/translate_darija_to_english1';
      } else if (language == 'English to Darija') {
        url = 'http://100.91.176.36:3000/translate_english_to_darija1';
      } else if (language == 'Assistant Trans') {
        url = 'http://100.91.176.36:3000/map_options';
      }

      var request = http.Request('POST', Uri.parse(url));

      request.headers.addAll({
        'Content-Type': 'application/json; charset=UTF-8',
      });

      request.body = jsonEncode({'sentence': text});

      var response = await http.Client().send(request);

      var responseBody = await response.stream.bytesToString();
      
      if (response.statusCode == 200) {
        return responseBody;
      } else {
        return 'Request error: ${response.statusCode}';
      }
    } catch (e) {
      return 'Connection error';
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          width: 400,
          height: 600,
          decoration: BoxDecoration(
            border: Border.all(color: kPrimaryColor),
            borderRadius: BorderRadius.circular(20),
            color: Colors.grey[200],
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              SizedBox(height: 20),
              Container(
                width: 380,
                child: DropdownButton<String>(
                  value: selectedLanguage,
                  onChanged: (newValue) {
                    setState(() {
                      selectedLanguage = newValue!;
                    });
                  },
                  items: languages.map<DropdownMenuItem<String>>((String value) {
                    return DropdownMenuItem<String>(
                      value: value,
                      child: Text(value),
                    );
                  }).toList(),
                ),
              ),
              SizedBox(height: 20),
              Container(
                width: 380,
                child: TextField(
                  controller: _textController,
                  keyboardType: TextInputType.text,
                  //maxLines: null, // Permet un nombre illimité de lignes
                  cursorColor: Colors.black,
                  style: TextStyle(color: Colors.black),
                  decoration: InputDecoration(
                    enabledBorder: OutlineInputBorder(
                      borderRadius: const BorderRadius.all(Radius.circular(20)),
                      borderSide: BorderSide(color: Colors.grey),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: const BorderRadius.all(Radius.circular(20)),
                      borderSide: BorderSide(color: Colors.grey),
                    ),
                    border: OutlineInputBorder(
                      borderRadius: const BorderRadius.all(Radius.circular(20)),
                      borderSide: BorderSide(color: Colors.grey),
                    ),
                    labelStyle: TextStyle(color: Colors.grey),
                    labelText: "Write here",
                    contentPadding: const EdgeInsets.symmetric(vertical: 10.0, horizontal: 10.0),
                  ),
                  onSubmitted: (value) {
                    _sendText();
                  },
                ),
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: _sendText, // Appeler la méthode d'envoi lorsque le bouton est pressé
                style: ElevatedButton.styleFrom(
                  backgroundColor: kPrimaryColor,
                  elevation: 14,
                ),
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Text(
                    'translite',
                    textAlign: TextAlign.end,
                    style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                ),
              ),
              SizedBox(height: 20),
              Container(
                width: 380,
                height: 300,
                padding: EdgeInsets.all(16),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey),
                  borderRadius: BorderRadius.circular(30),
                ),
                child: Center(
                  child: TextField(
                    readOnly: true,
                    expands: true,
                    keyboardType: TextInputType.multiline,
                    maxLines: null,
                    cursorColor: Colors.black,
                    style: TextStyle(color: Colors.black),
                    decoration: InputDecoration(
                      border: InputBorder.none,
                      contentPadding: EdgeInsets.zero,
                    ),
                    controller: TextEditingController(text: predictionResult),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}