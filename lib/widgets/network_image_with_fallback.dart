import 'package:flutter/material.dart';

class NetworkImageWithFallback extends StatelessWidget {
  const NetworkImageWithFallback({
    super.key,
    required this.url,
    this.height = 140,
  });

  final String url;
  final double height;

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(12),
      child: Image.network(
        url,
        height: height,
        width: double.infinity,
        fit: BoxFit.cover,
        loadingBuilder:
            (BuildContext context, Widget child, ImageChunkEvent? progress) {
              if (progress == null) {
                return child;
              }
              return SizedBox(
                height: height,
                child: const Center(child: CircularProgressIndicator()),
              );
            },
        errorBuilder:
            (BuildContext context, Object error, StackTrace? stackTrace) {
              return Container(
                height: height,
                color: Theme.of(context).colorScheme.surfaceContainerHighest,
                alignment: Alignment.center,
                child: const Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[
                    Icon(Icons.broken_image_outlined, size: 36),
                    SizedBox(height: 6),
                    Text('图片加载失败，已显示兜底视图'),
                  ],
                ),
              );
            },
      ),
    );
  }
}
