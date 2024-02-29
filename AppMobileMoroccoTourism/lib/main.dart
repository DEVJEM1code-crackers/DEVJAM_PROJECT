import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:travee/screens/homescreen/bottom_nav_bar.dart';
import 'package:travee/screens/homescreen/home_screen.dart';
import 'package:travee/screens/mainscreen/main_screen1.dart';
import 'package:travee/screens/mainscreen/main_screen2.dart';
import 'package:travee/screens/mainscreen/main_screen3.dart';

void main() {


  runApp(const MyApp()); // travee app
  //runApp(const DemoApp()); // animation class
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: 'travee',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      debugShowCheckedModeBanner: false,
      home: const MainScreen1(),
    );
  }
}
