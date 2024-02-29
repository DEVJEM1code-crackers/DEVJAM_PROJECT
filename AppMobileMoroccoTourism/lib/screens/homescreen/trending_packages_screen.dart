import 'package:flutter/material.dart';
import 'dart:io';
import 'package:image_picker/image_picker.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

import '../../resources/color.dart';

class TrendingPackagesScreen extends StatefulWidget {
  const TrendingPackagesScreen({Key? key}) : super(key: key);

  @override
  State<TrendingPackagesScreen> createState() => _TrendingPackagesScreenState();
}

class _TrendingPackagesScreenState extends State<TrendingPackagesScreen> {

  File? imageFile;
  bool _isUploaded = false;
  String predictionResult = 'hello';

  Future<void> _pickImage() async {
    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      setState(() {
        imageFile = File(pickedFile.path);
        _isUploaded = true;
        predictionResult = '';
      });

      sendImageAndGetResult(imageFile!).then((result) {
        setState(() {
          predictionResult = result;
        });
      }).catchError((error) {
        print('Erreur lors de l\'envoi de l\'image : $error');
      });
    }
  }

  Future<String> sendImageAndGetResult(File imageFile) async {
    var url = Uri.parse('http://100.91.176.36:3000/predict');
    List<int> imageBytes = await imageFile.readAsBytes();
    String base64Image = base64Encode(imageBytes);
    try {
      var response = await http.post(
        url,
        body: {
          'image': imageBytes,
        },
      );
      if (response.statusCode == 200) {
        return response.body;
      } else {
        return 'Erreur lors de la requête : ${response.statusCode}';
      }
    } catch (e) {
      return 'Erreur de connexion';
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            SizedBox(height: 20),
            imageFile != null
                ? Container(
              width: 200,
              height: 200,
              decoration: BoxDecoration(
                border: Border.all(color: kPrimaryColor),
                borderRadius: BorderRadius.circular(20),
              ),
              child: Stack(
                alignment: Alignment.center,
                children: [
                  Image.file(imageFile!, fit: BoxFit.cover),
                  if (_isUploaded)
                    Icon(
                      Icons.check_circle,
                      color: kWhiteColor,
                      size: 100,
                    ),
                ],
              ),
            )
                : Container(
              width: 200,
              height: 100,
              decoration: BoxDecoration(
                border: Border.all(color: kPrimaryColor ),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Center(child: Text('Aucune image')),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _pickImage,
              style: ElevatedButton.styleFrom(
                backgroundColor: kPrimaryColor, // Utilisez kPrimaryColor comme couleur de fond
                elevation: 14,
              ),
              child: Padding(
                padding: const EdgeInsets.all(16.0), // Ajoutez un espacement intérieur au texte du bouton
                child: Text(
                  'Uploader une image',
                  textAlign: TextAlign.end,
                  style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                ),
              ),
            ),

            SizedBox(height: 20),
            Container(
              width: 380,
              padding: EdgeInsets.all(16),
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Center(
                child: Text(predictionResult),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

